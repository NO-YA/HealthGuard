cat > backend/app/api/routes.py << 'EOF'
"""API routes"""
from flask import request, jsonify, current_app
from app.api import api_bp
from app.models import Patient, Analysis
from app.ml_service import MLService
from datetime import datetime
from werkzeug.utils import secure_filename
import os

ml_service = MLService()

# ==================== Health Check ====================

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return {
        'status': 'ok',
        'message': 'HealthGuard API is running',
        'timestamp': datetime.utcnow().isoformat()
    }, 200

# ==================== Patient Endpoints ====================

@api_bp.route('/patients', methods=['POST'])
def create_patient():
    """Create a new patient"""
    try:
        data = request.get_json()
        
        if not data or not data.get('email'):
            return {'error': 'Email is required'}, 400
        
        # Check if patient exists
        if Patient.objects(email=data['email']):
            return {'error': 'Patient already exists'}, 409
        
        patient = Patient(
            email=data['email'],
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            age=data.get('age'),
            gender=data.get('gender')
        )
        patient.save()
        
        return {
            'message': 'Patient created successfully',
            'patient_id': str(patient.id),
            'patient': patient.to_json()
        }, 201
        
    except Exception as e:
        current_app.logger.error(f"Error creating patient: {e}")
        return {'error': str(e)}, 500

@api_bp.route('/patients/<patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Get patient by ID"""
    try:
        from bson import ObjectId
        patient = Patient.objects(id=ObjectId(patient_id)).first()
        
        if not patient:
            return {'error': 'Patient not found'}, 404
        
        # Get patient's analyses
        analyses = Analysis.objects(patient=patient)
        
        return {
            'patient': patient.to_json(),
            'analyses_count': len(analyses),
            'last_analysis': analyses.first().created_at.isoformat() if analyses else None
        }, 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting patient: {e}")
        return {'error': str(e)}, 500

# ==================== Analysis Endpoints ====================

@api_bp.route('/analyze', methods=['POST'])
def analyze_image():
    """Upload and analyze image"""
    try:
        # Validate request
        if 'image' not in request.files:
            return {'error': 'No image file provided'}, 400
        
        if 'patient_id' not in request.form:
            return {'error': 'patient_id is required'}, 400
        
        image = request.files['image']
        patient_id = request.form['patient_id']
        
        # Validate image
        if image.filename == '':
            return {'error': 'No file selected'}, 400
        
        if not allowed_file(image.filename):
            return {'error': 'Invalid file format. Only JPG and PNG allowed'}, 400
        
        # Get patient
        from bson import ObjectId
        patient = Patient.objects(id=ObjectId(patient_id)).first()
        if not patient:
            return {'error': 'Patient not found'}, 404
        
        # Save image
        filename = secure_filename(image.filename)
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        image_path = os.path.join(upload_folder, filename)
        image.save(image_path)
        
        # Create analysis record (pending)
        analysis = Analysis(
            patient=patient,
            image_path=image_path,
            image_name=filename,
            status='pending'
        )
        analysis.save()
        
        # Run ML inference (in production, use async task)
        analysis.status = 'processing'
        analysis.save()
        
        try:
            start_time = datetime.utcnow()
            
            # Run predictions
            results = ml_service.predict_all(image_path)
            
            processing_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            # Update analysis with results
            analysis.status = 'completed'
            analysis.results = results
            analysis.completed_at = datetime.utcnow()
            analysis.processing_time_ms = processing_time
            analysis.save()
            
        except Exception as e:
            current_app.logger.error(f"ML inference error: {e}")
            analysis.status = 'error'
            analysis.error_message = str(e)
            analysis.save()
            return {
                'analysis_id': str(analysis.id),
                'status': 'error',
                'error': str(e)
            }, 500
        
        return {
            'analysis_id': str(analysis.id),
            'status': analysis.status,
            'results': analysis.results,
            'processing_time_ms': analysis.processing_time_ms
        }, 200
        
    except Exception as e:
        current_app.logger.error(f"Error analyzing image: {e}")
        return {'error': str(e)}, 500

@api_bp.route('/analysis/<analysis_id>', methods=['GET'])
def get_analysis(analysis_id):
    """Get analysis results"""
    try:
        from bson import ObjectId
        analysis = Analysis.objects(id=ObjectId(analysis_id)).first()
        
        if not analysis:
            return {'error': 'Analysis not found'}, 404
        
        return {
            'analysis': analysis.to_json()
        }, 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting analysis: {e}")
        return {'error': str(e)}, 500

@api_bp.route('/patients/<patient_id>/analyses', methods=['GET'])
def get_patient_analyses(patient_id):
    """Get all analyses for a patient"""
    try:
        from bson import ObjectId
        patient = Patient.objects(id=ObjectId(patient_id)).first()
        
        if not patient:
            return {'error': 'Patient not found'}, 404
        
        analyses = Analysis.objects(patient=patient).order_by('-created_at')
        
        return {
            'patient_id': patient_id,
            'analyses_count': len(analyses),
            'analyses': [a.to_json() for a in analyses]
        }, 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting analyses: {e}")
        return {'error': str(e)}, 500

# ==================== Utility Functions ====================

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in \
           current_app.config['ALLOWED_EXTENSIONS']
EOF