// src/components/auth/AuthComponents.tsx - Simple Auth Components
import React from 'react';

// Simple placeholder components for now - just to fix imports
export const AuthPage: React.FC = () => {
  return (
    <div className="container mx-auto mt-10 max-w-md">
      <div className="bg-white rounded-lg shadow-md p-6 text-center">
        <h2 className="text-2xl font-semibold mb-4">🎯 Hebrew AI Platform</h2>
        <p className="text-gray-600 mb-6">
          Authentication system coming soon!
        </p>
        <div className="text-sm text-gray-500">
          For now, access the study page directly
        </div>
      </div>
    </div>
  );
};

export const AuthModal: React.FC<{show: boolean; onHide: () => void; onAuthSuccess: () => void}> = () => {
  return <div>Auth Modal Coming Soon</div>;
};

export const UserProfile: React.FC<{onClose: () => void}> = () => {
  return <div>User Profile Coming Soon</div>;
};