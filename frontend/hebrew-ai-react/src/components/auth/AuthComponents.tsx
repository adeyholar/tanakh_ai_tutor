// src/components/auth/AuthComponents.tsx - Authentication Components
import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { Modal, Button } from 'react-bootstrap'; // Assuming Bootstrap is installed

export const AuthPage: React.FC = () => {
  const { register, login } = useAuth();
  const [isLogin, setIsLogin] = useState(true);
  const [credentials, setCredentials] = useState({ username: '', email: '', password: '' });
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCredentials({ ...credentials, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      if (isLogin) {
        const result = await login({ username: credentials.username, password: credentials.password });
        if (result.success) window.location.href = '/';
        else setError(result.error || 'Login failed');
      } else {
        const result = await register({ ...credentials, learning_level: 'beginner' });
        if (result.success) window.location.href = '/';
        else setError(result.error || 'Registration failed');
      }
    } catch (err) {
      setError((err as Error).message || 'An error occurred');
    }
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <div className="card">
            <div className="card-body">
              <h2 className="card-title text-center">{isLogin ? 'Login' : 'Register'}</h2>
              {error && <div className="alert alert-danger">{error}</div>}
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label htmlFor="username" className="form-label">Username</label>
                  <input
                    type="text"
                    className="form-control"
                    id="username"
                    name="username"
                    value={credentials.username}
                    onChange={handleChange}
                    required
                  />
                </div>
                {!isLogin && (
                  <div className="mb-3">
                    <label htmlFor="email" className="form-label">Email</label>
                    <input
                      type="email"
                      className="form-control"
                      id="email"
                      name="email"
                      value={credentials.email}
                      onChange={handleChange}
                      required
                    />
                  </div>
                )}
                <div className="mb-3">
                  <label htmlFor="password" className="form-label">Password</label>
                  <input
                    type="password"
                    className="form-control"
                    id="password"
                    name="password"
                    value={credentials.password}
                    onChange={handleChange}
                    required
                  />
                </div>
                <button type="submit" className="btn btn-primary w-100">{isLogin ? 'Login' : 'Register'}</button>
                <div className="text-center mt-3">
                  <button
                    type="button"
                    className="btn btn-link"
                    onClick={() => setIsLogin(!isLogin)}
                  >
                    {isLogin ? 'Need an account? Register' : 'Already have an account? Login'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export const AuthModal: React.FC<{ show: boolean; onHide: () => void; onAuthSuccess: () => void }> = ({ show, onHide, onAuthSuccess }) => {
  const { register, login } = useAuth();
  const [isLogin, setIsLogin] = useState(true);
  const [credentials, setCredentials] = useState({ username: '', email: '', password: '' });
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCredentials({ ...credentials, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      if (isLogin) {
        const result = await login({ username: credentials.username, password: credentials.password });
        if (result.success) {
          onAuthSuccess();
          onHide();
        } else {
          setError(result.error || 'Login failed');
        }
      } else {
        const result = await register({ ...credentials, learning_level: 'beginner' });
        if (result.success) {
          onAuthSuccess();
          onHide();
        } else {
          setError(result.error || 'Registration failed');
        }
      }
    } catch (err) {
      setError((err as Error).message || 'An error occurred');
    }
  };

  return (
    <Modal show={show} onHide={onHide} centered>
      <Modal.Header closeButton>
        <Modal.Title>{isLogin ? 'Login' : 'Register'}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {error && <div className="alert alert-danger">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="username" className="form-label">Username</label>
            <input
              type="text"
              className="form-control"
              id="username"
              name="username"
              value={credentials.username}
              onChange={handleChange}
              required
            />
          </div>
          {!isLogin && (
            <div className="mb-3">
              <label htmlFor="email" className="form-label">Email</label>
              <input
                type="email"
                className="form-control"
                id="email"
                name="email"
                value={credentials.email}
                onChange={handleChange}
                required
              />
            </div>
          )}
          <div className="mb-3">
            <label htmlFor="password" className="form-label">Password</label>
            <input
              type="password"
              className="form-control"
              id="password"
              name="password"
              value={credentials.password}
              onChange={handleChange}
              required
            />
          </div>
          <Button variant="primary" type="submit">{isLogin ? 'Login' : 'Register'}</Button>
          <div className="text-center mt-3">
            <Button
              variant="link"
              onClick={() => setIsLogin(!isLogin)}
            >
              {isLogin ? 'Need an account? Register' : 'Already have an account? Login'}
            </Button>
          </div>
        </form>
      </Modal.Body>
    </Modal>
  );
};

export const UserProfile: React.FC<{ onClose: () => void }> = ({ onClose }) => {
  const { user, getUserProfile, updateProfile } = useAuth();
  const [profile, setProfile] = useState<User | null>(null);
  const [editMode, setEditMode] = useState(false);
  const [updates, setUpdates] = useState<Partial<User>>({});
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    const profileData = await getUserProfile();
    setProfile(profileData);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUpdates({ ...updates, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      const result = await updateProfile(updates);
      if (result.success) {
        setEditMode(false);
        await loadProfile();
      } else {
        setError('Update failed');
      }
    } catch (err) {
      setError((err as Error).message || 'An error occurred');
    }
  };

  return (
    <Modal show={true} onHide={onClose} centered>
      <Modal.Header closeButton>
        <Modal.Title>User Profile</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {error && <div className="alert alert-danger">{error}</div>}
        {profile ? (
          editMode ? (
            <form onSubmit={handleSubmit}>
              <div className="mb-3">
                <label htmlFor="username" className="form-label">Username</label>
                <input
                  type="text"
                  className="form-control"
                  id="username"
                  name="username"
                  defaultValue={profile.username}
                  onChange={handleChange}
                />
              </div>
              <div className="mb-3">
                <label htmlFor="email" className="form-label">Email</label>
                <input
                  type="email"
                  className="form-control"
                  id="email"
                  name="email"
                  defaultValue={profile.email}
                  onChange={handleChange}
                />
              </div>
              <Button variant="primary" type="submit">Save Changes</Button>
              <Button variant="secondary" className="ms-2" onClick={() => setEditMode(false)}>Cancel</Button>
            </form>
          ) : (
            <div>
              <p><strong>Username:</strong> {profile.username}</p>
              <p><strong>Email:</strong> {profile.email}</p>
              <p><strong>Level:</strong> {profile.learning_level}</p>
              <p><strong>Study Time:</strong> {profile.total_study_time || 0} min</p>
              <p><strong>Words Learned:</strong> {profile.words_learned || 0}</p>
              <Button variant="primary" onClick={() => setEditMode(true)}>Edit Profile</Button>
            </div>
          )
        ) : (
          <div>Loading profile...</div>
        )}
      </Modal.Body>
    </Modal>
  );
};