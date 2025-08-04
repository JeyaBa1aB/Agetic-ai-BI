"""
File upload routes for Multi-Agent BI Assistant
Handles CSV file uploads and validation
"""
import os
import logging
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import pandas as pd
from config.settings import Config

logger = logging.getLogger(__name__)

# Create blueprint
upload_bp = Blueprint('upload', __name__)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def validate_csv_file(file_path):
    """Validate CSV file structure and content"""
    try:
        # Read CSV file with fallback encoding
        encoding = getattr(Config, 'CSV_ENCODING', 'utf-8')
        df = pd.read_csv(file_path, encoding=encoding)
        
        # Basic validation
        if df.empty:
            return False, "CSV file is empty"
        
        if len(df.columns) == 0:
            return False, "CSV file has no columns"
        
        # Check for minimum data requirements
        if len(df) < 2:
            return False, "CSV file must contain at least 2 rows of data"
        
        # Get basic info about the dataset
        info = {
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': df.columns.tolist(),
            'data_types': {str(k): str(v) for k, v in df.dtypes.to_dict().items()},
            'memory_usage': int(df.memory_usage(deep=True).sum()),
            'has_null_values': bool(df.isnull().any().any()),
            'null_counts': {str(k): int(v) for k, v in df.isnull().sum().to_dict().items()}
        }
        
        return True, info
        
    except pd.errors.EmptyDataError:
        return False, "CSV file is empty or corrupted"
    except pd.errors.ParserError as e:
        return False, f"CSV parsing error: {str(e)}"
    except UnicodeDecodeError:
        return False, f"Encoding error. Expected {Config.CSV_ENCODING} encoding"
    except Exception as e:
        return False, f"Validation error: {str(e)}"

@upload_bp.route('/file', methods=['POST'])
def upload_file():
    """Upload and validate CSV file"""
    try:
        # Check if file is present in request
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Check file extension
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': f'File type not allowed. Allowed extensions: {Config.ALLOWED_EXTENSIONS}'
            }), 400
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > Config.MAX_FILE_SIZE:
            return jsonify({
                'success': False,
                'error': f'File too large. Maximum size: {Config.MAX_FILE_SIZE / (1024*1024):.1f}MB'
            }), 400
        
        # Secure filename
        filename = secure_filename(file.filename)
        
        # Create temporary file path
        temp_dir = os.path.join(os.path.dirname(__file__), '..', 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, filename)
        
        # Save file temporarily
        file.save(file_path)
        
        try:
            # Validate CSV file
            is_valid, validation_result = validate_csv_file(file_path)
            
            if not is_valid:
                return jsonify({
                    'success': False,
                    'error': validation_result
                }), 400
            
            # Read file content for processing
            encoding = getattr(Config, 'CSV_ENCODING', 'utf-8')
            with open(file_path, 'r', encoding=encoding) as f:
                csv_content = f.read()
            
            # Clean up temporary file
            os.remove(file_path)
            
            logger.info(f"File uploaded successfully: {filename} ({file_size} bytes)")
            
            return jsonify({
                'success': True,
                'message': 'File uploaded and validated successfully',
                'file_info': {
                    'filename': filename,
                    'size': file_size,
                    'size_mb': round(file_size / (1024*1024), 2),
                    **validation_result
                },
                'csv_content': csv_content
            })
            
        except Exception as e:
            # Clean up temporary file on error
            if os.path.exists(file_path):
                os.remove(file_path)
            raise e
            
    except Exception as e:
        logger.error(f"File upload error: {e}")
        return jsonify({
            'success': False,
            'error': f'Upload failed: {str(e)}'
        }), 500

@upload_bp.route('/validate', methods=['POST'])
def validate_csv_data():
    """Validate CSV data sent as text"""
    try:
        data = request.get_json()
        
        if not data or ('csv_content' not in data and 'csv_data' not in data):
            return jsonify({
                'success': False,
                'error': 'No CSV content provided'
            }), 400
        
        # Support both csv_content and csv_data for compatibility
        csv_content = data.get('csv_content') or data.get('csv_data')
        
        # Create temporary file for validation
        temp_dir = os.path.join(os.path.dirname(__file__), '..', 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        temp_file = os.path.join(temp_dir, 'temp_validation.csv')
        
        try:
            # Write content to temporary file
            encoding = getattr(Config, 'CSV_ENCODING', 'utf-8')
            with open(temp_file, 'w', encoding=encoding) as f:
                f.write(csv_content)
            
            # Validate the file
            is_valid, validation_result = validate_csv_file(temp_file)
            
            # Clean up
            os.remove(temp_file)
            
            if not is_valid:
                return jsonify({
                    'success': False,
                    'error': validation_result
                }), 400
            
            return jsonify({
                'success': True,
                'message': 'CSV data is valid',
                'validation_info': validation_result
            })
            
        except Exception as e:
            # Clean up on error
            if os.path.exists(temp_file):
                os.remove(temp_file)
            raise e
            
    except Exception as e:
        logger.error(f"CSV validation error: {e}")
        return jsonify({
            'success': False,
            'error': f'Validation failed: {str(e)}'
        }), 500

@upload_bp.route('/info', methods=['GET'])
def upload_info():
    """Get upload configuration information"""
    return jsonify({
        'max_file_size': Config.MAX_FILE_SIZE,
        'max_file_size_mb': Config.MAX_FILE_SIZE / (1024*1024),
        'allowed_extensions': Config.ALLOWED_EXTENSIONS,
        'encoding': Config.CSV_ENCODING
    })