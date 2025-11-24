import { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext(null);

// Create axios instance with interceptor for JWT
const apiClient = axios.create({
  baseURL: 'http://localhost:5000'
});

// Add request interceptor to include token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('teacher_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [teacher, setTeacher] = useState(null);
  const [loading, setLoading] = useState(true);

  // Load teacher profile on mount if token exists
  useEffect(() => {
    const loadTeacher = async () => {
      const token = localStorage.getItem('teacher_token');
      if (token) {
        try {
          const response = await apiClient.get('/api/teacher/profile');
          if (response.data.status === 'success') {
            setTeacher(response.data.teacher);
          }
        } catch (error) {
          console.error('Failed to load teacher profile:', error);
          // Token is invalid, clear it
          localStorage.removeItem('teacher_token');
          setTeacher(null);
        }
      }
      setLoading(false);
    };

    loadTeacher();
  }, []);

  const login = async (username, password) => {
    try {
      const response = await apiClient.post('/api/teacher/login', {
        username,
        password
      });

      if (response.data.status === 'success') {
        const { access_token, teacher: teacherData } = response.data;

        // Save token to localStorage
        localStorage.setItem('teacher_token', access_token);
        setTeacher(teacherData);

        return { success: true };
      } else {
        return { success: false, message: response.data.message };
      }
    } catch (error) {
      console.error('Login error:', error);
      return {
        success: false,
        message: error.response?.data?.message || 'Login failed. Please try again.'
      };
    }
  };

  const logout = () => {
    localStorage.removeItem('teacher_token');
    setTeacher(null);
  };

  const value = {
    teacher,
    loading,
    isAuthenticated: !!teacher,
    login,
    logout
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Export apiClient for use in components
export { apiClient };
