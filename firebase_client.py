"""
Firebase Firestore Client for AETP
Manages strategy storage, performance tracking, and real-time updates
"""
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from datetime import datetime, timedelta
import logging
import json
from typing import Dict, Any, List, Optional, Generator
import time

class FirestoreClient:
    """Firebase Firestore client for AETP"""
    
    def __init__(self):
        self._initialized = False
        self.db = None
        self._initialize_firebase()
    
    def _initialize_firebase(self) -> bool:
        """Initialize Firebase Admin SDK"""
        try:
            # Check if Firebase app already exists
            if not firebase_admin._apps:
                # Initialize with service account credentials
                cred_path = "service_account_key.json"
                
                # Verify file exists before attempting to read
                import os
                if not os.path.exists(cred_path):
                    logging.error(f"Firebase service account file not found: {cred_path}")
                    logging.info("Attempting to use environment variable GOOGLE_APPLICATION_CREDENTIALS")
                    # Rely on environment variable if file doesn't exist
                    cred