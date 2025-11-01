import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  TextInput,
  ScrollView,
  Alert,
  Dimensions,
  Modal,
  FlatList,
  StatusBar,
  ActivityIndicator,
  Image,
  Animated,
} from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import * as Location from 'expo-location';
import { Magnetometer } from 'expo-sensors';
import * as ImagePicker from 'expo-image-picker';
import { createClient } from '@supabase/supabase-js';

// Supabase Configuration - Replace with your actual credentials
const supabaseUrl = 'https://rwmjevyosxqwyxhsmfda.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ3bWpldnlvc3hxd3l4aHNtZmRhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ0MjU4NzksImV4cCI6MjA3MDAwMTg3OX0.sELr9vsvi4BwaUUq0ldUuDuSh7JVTH8TW-YpwFk5c_Y';

const supabase = createClient(supabaseUrl, supabaseKey);

const Tab = createBottomTabNavigator();
const { width, height } = Dimensions.get('window');

// Super Admin Email and Password - Only this account can approve moderators
const SUPER_ADMIN_EMAIL = 'abhiramgunda8@gmail.com';
const SUPER_ADMIN_PASSWORD = 'divyaviswanath';

// US Schools Data
const US_SCHOOLS = [
  { id: 1, name: 'Lincoln High School', state: 'CA' },
  { id: 2, name: 'Washington Middle School', state: 'TX' },
  { id: 3, name: 'Roosevelt High School', state: 'NY' },
  { id: 4, name: 'Jefferson Middle School', state: 'FL' },
  { id: 5, name: 'Kennedy High School', state: 'IL' },
  { id: 6, name: 'Adams Middle School', state: 'PA' },
  { id: 7, name: 'Madison High School', state: 'OH' },
  { id: 8, name: 'Monroe Middle School', state: 'GA' },
  { id: 9, name: 'Jackson High School', state: 'NC' },
  { id: 10, name: 'Van Buren Middle School', state: 'MI' },
  { id: 11, name: 'Harrison High School', state: 'NJ' },
  { id: 12, name: 'Tyler Middle School', state: 'VA' },
  { id: 13, name: 'Polk High School', state: 'WA' },
  { id: 14, name: 'Taylor Middle School', state: 'AZ' },
  { id: 15, name: 'Fillmore High School', state: 'MA' },
  { id: 16, name: 'Pierce Middle School', state: 'TN' },
  { id: 17, name: 'Buchanan High School', state: 'MO' },
  { id: 18, name: 'Johnson Middle School', state: 'MD' },
  { id: 19, name: 'Grant High School', state: 'WI' },
  { id: 20, name: 'Hayes Middle School', state: 'MN' },
  { id: 21, name: 'Garfield High School', state: 'CO' },
  { id: 22, name: 'Arthur Middle School', state: 'AL' },
  { id: 23, name: 'Cleveland High School', state: 'SC' },
  { id: 24, name: 'McKinley Middle School', state: 'LA' },
  { id: 25, name: 'Wilson High School', state: 'KY' },
  { id: 26, name: 'Taft Middle School', state: 'OR' },
  { id: 27, name: 'Harding High School', state: 'OK' },
  { id: 28, name: 'Coolidge Middle School', state: 'CT' },
  { id: 29, name: 'Hoover High School', state: 'IA' },
  { id: 30, name: 'Truman Middle School', state: 'KS' },
  { id: 31, name: 'Eisenhower High School', state: 'AR' },
  { id: 32, name: 'Reagan Middle School', state: 'MS' },
  { id: 33, name: 'Bush High School', state: 'UT' },
  { id: 34, name: 'Clinton Middle School', state: 'NV' },
  { id: 35, name: 'Obama High School', state: 'NM' },
  { id: 36, name: 'Central High School', state: 'WV' },
  { id: 37, name: 'North Middle School', state: 'NE' },
  { id: 38, name: 'South High School', state: 'ID' },
  { id: 39, name: 'East Middle School', state: 'NH' },
  { id: 40, name: 'West High School', state: 'ME' },
  { id: 41, name: 'Riverside High School', state: 'HI' },
  { id: 42, name: 'Sunset Middle School', state: 'AK' },
  { id: 43, name: 'Mountain View High School', state: 'MT' },
  { id: 44, name: 'Valley Middle School', state: 'ND' },
  { id: 45, name: 'Hillcrest High School', state: 'SD' },
  { id: 46, name: 'Oakwood Middle School', state: 'WY' },
  { id: 47, name: 'Pine Ridge High School', state: 'VT' },
  { id: 48, name: 'Cedar Creek Middle School', state: 'DE' },
  { id: 49, name: 'Maple Grove High School', state: 'RI' },
  { id: 50, name: 'Willow Springs Middle School', state: 'DC' },
];

// Utility Functions
const generateId = () => Math.random().toString(36).substr(2, 9);

const calculateDistance = (lat1, lon1, lat2, lon2) => {
  const R = 6371e3;
  const φ1 = (lat1 * Math.PI) / 180;
  const φ2 = (lat2 * Math.PI) / 180;
  const Δφ = ((lat2 - lat1) * Math.PI) / 180;
  const Δλ = ((lon2 - lon1) * Math.PI) / 180;

  const a =
    Math.sin(Δφ / 2) * Math.sin(Δφ / 2) +
    Math.cos(φ1) * Math.cos(φ2) * Math.sin(Δλ / 2) * Math.sin(Δλ / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

  return R * c;
};

const calculateBearing = (lat1, lon1, lat2, lon2) => {
  const φ1 = (lat1 * Math.PI) / 180;
  const φ2 = (lat2 * Math.PI) / 180;
  const Δλ = ((lon2 - lon1) * Math.PI) / 180;

  const y = Math.sin(Δλ) * Math.cos(φ2);
  const x =
    Math.cos(φ1) * Math.sin(φ2) - Math.sin(φ1) * Math.cos(φ2) * Math.cos(Δλ);

  const θ = Math.atan2(y, x);
  return ((θ * 180) / Math.PI + 360) % 360;
};

// Main App Component
export default function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkUser();
  }, []);

  const checkUser = async () => {
    try {
      const {
        data: { user: authUser },
      } = await supabase.auth.getUser();
      
      if (authUser) {
        const { data: userData } = await supabase
          .from('users')
          .select('*')
          .eq('id', authUser.id)
          .single();

        if (userData) {
          setUser(userData);
        } else {
          await supabase.auth.signOut();
        }
      }
    } catch (error) {
      console.error('Error checking user:', error);
      await supabase.auth.signOut();
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View style={[styles.container, styles.centered]}>
        <ActivityIndicator size="large" color="#00ff00" />
        <Text style={styles.loadingText}>Loading Hitlist...</Text>
      </View>
    );
  }

  if (!user) {
    return <AuthScreen onAuth={setUser} />;
  }

  // Check user status
  if (user.banned) {
    return (
      <View style={[styles.container, styles.centered]}>
        <Text style={styles.bannedTitle}>🚫 ACCOUNT BANNED</Text>
        <Text style={styles.bannedText}>Your account has been banned by a moderator.</Text>
        <TouchableOpacity 
          style={styles.button}
          onPress={async () => {
            await supabase.auth.signOut();
            setUser(null);
          }}
        >
          <Text style={styles.buttonText}>SIGN OUT</Text>
        </TouchableOpacity>
      </View>
    );
  }

  if (user.timeout_until && new Date(user.timeout_until) > new Date()) {
    const timeLeft = Math.ceil((new Date(user.timeout_until) - new Date()) / (1000 * 60));
    return (
      <View style={[styles.container, styles.centered]}>
        <Text style={styles.timeoutTitle}>⏰ TIMEOUT ACTIVE</Text>
        <Text style={styles.timeoutText}>You are timed out for {timeLeft} minutes.</Text>
        <TouchableOpacity 
          style={styles.button}
          onPress={async () => {
            await supabase.auth.signOut();
            setUser(null);
          }}
        >
          <Text style={styles.buttonText}>SIGN OUT</Text>
        </TouchableOpacity>
      </View>
    );
  }

  if (!user.verified && user.email !== SUPER_ADMIN_EMAIL) {
    return <UnverifiedScreen user={user} onAuth={setUser} />;
  }

  return (
    <NavigationContainer>
      <StatusBar barStyle="light-content" backgroundColor="#0a0a0a" />
      <Tab.Navigator
        screenOptions={{
          tabBarStyle: styles.tabBar,
          tabBarActiveTintColor: '#00ff00',
          tabBarInactiveTintColor: '#666',
          headerStyle: styles.header,
          headerTintColor: '#00ff00',
          headerTitleStyle: styles.headerTitle,
        }}>
        <Tab.Screen
          name="Compass"
          children={() => <CompassScreen user={user} />}
          options={{ tabBarLabel: '🧭 Hunt' }}
        />
        <Tab.Screen
          name="Action"
          children={() => <ActionScreen user={user} setUser={setUser} />}
          options={{ tabBarLabel: '⚡ Action' }}
        />
        <Tab.Screen
          name="Leaderboard"
          children={() => <LeaderboardScreen user={user} />}
          options={{ tabBarLabel: '🏆 Ranks' }}
        />
        <Tab.Screen
          name="Chat"
          children={() => <ChatScreen user={user} />}
          options={{ tabBarLabel: '💬 Chat' }}
        />
        {(user.role === 'moderator' || user.email === SUPER_ADMIN_EMAIL) && (
          <Tab.Screen
            name="Moderator"
            children={() => <ModeratorScreen user={user} />}
            options={{ tabBarLabel: '🛡️ Admin' }}
          />
        )}
      </Tab.Navigator>
    </NavigationContainer>
  );
}

// Auth Screen Component
function AuthScreen({ onAuth }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [selectedSchool, setSelectedSchool] = useState(null);
  const [showSchools, setShowSchools] = useState(false);
  const [step, setStep] = useState('login');
  const [loading, setLoading] = useState(false);
  const [photoUri, setPhotoUri] = useState(null);
  const [accountType, setAccountType] = useState('player');

  const handleLogin = async () => {
    if (!email || !password) {
      Alert.alert('Error', 'Please enter email and password');
      return;
    }

    setLoading(true);
    try {
      // Check if this is the super admin with hardcoded credentials
      if (email.trim().toLowerCase() === SUPER_ADMIN_EMAIL.toLowerCase() && password === SUPER_ADMIN_PASSWORD) {
        console.log('Super admin login detected');
        
        // First, check if super admin exists in database
        const { data: superAdminUser } = await supabase
          .from('users')
          .select('*')
          .eq('email', email.trim().toLowerCase())
          .single();

        if (superAdminUser) {
          // Super admin exists in database, log them in directly
          console.log('Super admin found in database, logging in...');
          onAuth(superAdminUser);
          return;
        } else {
          // Super admin doesn't exist in database yet
          Alert.alert(
            'Super Admin Setup', 
            'Super admin account not found. Please create it through signup first.',
            [
              { text: 'OK' },
              { 
                text: 'Go to Signup', 
                onPress: () => setStep('signup') 
              }
            ]
          );
          return;
        }
      }

      // Regular user login through Supabase auth
      const { data, error } = await supabase.auth.signInWithPassword({
        email: email.trim(),
        password: password,
      });

      if (error) throw error;

      if (data.user) {
        const { data: userData } = await supabase
          .from('users')
          .select('*')
          .eq('id', data.user.id)
          .single();

        if (userData) {
          onAuth(userData);
        } else {
          Alert.alert('Error', 'User profile not found');
          await supabase.auth.signOut();
        }
      }

    } catch (error) {
      console.error('Login error:', error);
      Alert.alert('Login Failed', error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSignup = async () => {
    if (!email || !password || !name) {
      Alert.alert('Error', 'Please fill in all fields');
      return;
    }

    if (password.length < 6) {
      Alert.alert('Error', 'Password must be at least 6 characters');
      return;
    }

    // For super admin, bypass the password check since we want to use the hardcoded one
    const isSuperAdmin = email.trim().toLowerCase() === SUPER_ADMIN_EMAIL.toLowerCase();
    
    if (isSuperAdmin) {
      // For super admin, just proceed to photo step directly (skip school selection)
      setAccountType('super_admin'); // Set a special account type
      setStep('photo');
    } else if (accountType === 'player') {
      setStep('school');
    } else {
      setStep('photo');
    }
  };

  const handleCompleteSignup = async () => {
    const isSuperAdmin = email.trim().toLowerCase() === SUPER_ADMIN_EMAIL.toLowerCase();
    
    if (!isSuperAdmin && accountType === 'player' && !selectedSchool) {
      Alert.alert('Error', 'Please select your school');
      return;
    }
    
    if (!photoUri) {
      Alert.alert('Error', 'Please upload a photo');
      return;
    }

    setLoading(true);
    try {
      let authUser = null;
      let userId = null;

      if (isSuperAdmin) {
        // For super admin, create a manual user ID and skip Supabase auth
        userId = 'super_admin_' + generateId(); // Generate a custom ID for super admin
        console.log('Creating super admin with manual ID:', userId);
      } else {
        // Regular user signup through Supabase auth
        const { data, error } = await supabase.auth.signUp({
          email: email.trim(),
          password: password,
        });

        if (error) throw error;
        if (!data.user) throw new Error('Failed to create account');
        
        authUser = data.user;
        userId = authUser.id;
      }

      // Determine user role
      let userRole = 'player';
      if (isSuperAdmin) {
        userRole = 'super_admin';
      } else if (accountType === 'moderator') {
        userRole = 'pending_mod';
      }

      // Handle server assignment for players
      let serverId = null;
      if (accountType === 'player' && selectedSchool) {
        let { data: server } = await supabase
          .from('servers')
          .select('*')
          .eq('school_id', selectedSchool.id)
          .single();

        if (!server) {
          const expiresAt = new Date();
          expiresAt.setDate(expiresAt.getDate() + 2);
          
          const { data: newServer } = await supabase
            .from('servers')
            .insert({ 
              school_id: selectedSchool.id,
              expires_at: expiresAt.toISOString()
            })
            .select()
            .single();
          server = newServer;
        }
        serverId = server.id;
      }

      // Create user in database
      const { data: newUser, error: userError } = await supabase
        .from('users')
        .insert({
          id: userId,
          name: name.trim(),
          email: email.trim().toLowerCase(),
          school_id: (accountType === 'player' && selectedSchool) ? selectedSchool.id : null,
          server_id: serverId,
          photo_url: photoUri,
          verified: isSuperAdmin, // Super admin is automatically verified
          banned: false,
          timeout_until: null,
          is_alive: true,
          kills: 0,
          points: 0,
          target_id: null,
          shield_until: null,
          last_lat: null,
          last_lng: null,
          role: userRole,
        })
        .select()
        .single();

      if (userError) throw userError;

      Alert.alert('Success!', 'Account created successfully.');
      onAuth(newUser);

    } catch (error) {
      console.error('Signup error:', error);
      Alert.alert('Signup Failed', error.message);
    } finally {
      setLoading(false);
    }
  };

  const selectPhoto = async () => {
    try {
      const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
      if (status !== 'granted') {
        Alert.alert('Permission Required', 'Please grant camera roll permissions.');
        return;
      }

      const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: true,
        aspect: [4, 3],
        quality: 0.8,
      });

      if (!result.canceled && result.assets[0]) {
        setPhotoUri(result.assets[0].uri);
      }
    } catch (error) {
      console.error('Photo selection error:', error);
      Alert.alert('Error', 'Failed to select photo');
    }
  };

  if (step === 'login') {
    return (
      <View style={styles.authContainer}>
        <Text style={styles.title}>🎯 HITLIST</Text>
        <Text style={styles.subtitle}>Welcome Back</Text>
        
        <TextInput
          style={styles.input}
          placeholder="Email"
          placeholderTextColor="#666"
          value={email}
          onChangeText={setEmail}
          keyboardType="email-address"
          autoCapitalize="none"
        />
        
        <TextInput
          style={styles.input}
          placeholder="Password"
          placeholderTextColor="#666"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />
        
        <TouchableOpacity 
          style={[styles.button, loading && styles.buttonDisabled]} 
          onPress={handleLogin}
          disabled={loading}
        >
          <Text style={styles.buttonText}>
            {loading ? 'SIGNING IN...' : 'SIGN IN'}
          </Text>
        </TouchableOpacity>
        
        <TouchableOpacity onPress={() => setStep('signup')}>
          <Text style={styles.linkText}>New user? Create account →</Text>
        </TouchableOpacity>
      </View>
    );
  }

  if (step === 'signup') {
    return (
      <View style={styles.authContainer}>
        <Text style={styles.title}>🎯 HITLIST</Text>
        <Text style={styles.subtitle}>Create New Account</Text>
        
        <View style={styles.accountTypeSelector}>
          <TouchableOpacity
            style={[styles.typeButton, accountType === 'player' && styles.typeButtonActive]}
            onPress={() => setAccountType('player')}
          >
            <Text style={[styles.typeButtonText, accountType === 'player' && styles.typeButtonTextActive]}>
              Player
            </Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.typeButton, accountType === 'moderator' && styles.typeButtonActive]}
            onPress={() => setAccountType('moderator')}
          >
            <Text style={[styles.typeButtonText, accountType === 'moderator' && styles.typeButtonTextActive]}>
              Moderator
            </Text>
          </TouchableOpacity>
        </View>
        
        <TextInput
          style={styles.input}
          placeholder="Full Name"
          placeholderTextColor="#666"
          value={name}
          onChangeText={setName}
          autoCapitalize="words"
        />
        
        <TextInput
          style={styles.input}
          placeholder="Email"
          placeholderTextColor="#666"
          value={email}
          onChangeText={setEmail}
          keyboardType="email-address"
          autoCapitalize="none"
        />
        
        <TextInput
          style={styles.input}
          placeholder={
            email.trim().toLowerCase() === SUPER_ADMIN_EMAIL.toLowerCase() 
              ? "Password (super admin)" 
              : "Password (min 6 characters)"
          }
          placeholderTextColor="#666"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />
        
        <TouchableOpacity style={styles.button} onPress={handleSignup}>
          <Text style={styles.buttonText}>CONTINUE</Text>
        </TouchableOpacity>
        
        <TouchableOpacity onPress={() => setStep('login')}>
          <Text style={styles.linkText}>← Back to login</Text>
        </TouchableOpacity>
      </View>
    );
  }

  if (step === 'school') {
    return (
      <View style={styles.authContainer}>
        <Text style={styles.title}>🎯 HITLIST</Text>
        <Text style={styles.subtitle}>Select Your School</Text>
        
        <TouchableOpacity 
          style={styles.schoolSelector}
          onPress={() => setShowSchools(true)}
        >
          <Text style={styles.schoolSelectorText}>
            {selectedSchool ? selectedSchool.name : 'Choose School'}
          </Text>
        </TouchableOpacity>

        {selectedSchool && (
          <TouchableOpacity style={styles.button} onPress={() => setStep('photo')}>
            <Text style={styles.buttonText}>CONTINUE</Text>
          </TouchableOpacity>
        )}

        <Modal visible={showSchools} animationType="slide">
          <View style={styles.modalContainer}>
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>Select School</Text>
              <TouchableOpacity onPress={() => setShowSchools(false)}>
                <Text style={styles.closeButton}>✕</Text>
              </TouchableOpacity>
            </View>
            <FlatList
              data={US_SCHOOLS}
              keyExtractor={(item) => item.id.toString()}
              renderItem={({ item }) => (
                <TouchableOpacity
                  style={styles.schoolItem}
                  onPress={() => {
                    setSelectedSchool(item);
                    setShowSchools(false);
                  }}
                >
                  <Text style={styles.schoolName}>{item.name}</Text>
                  <Text style={styles.schoolState}>{item.state}</Text>
                </TouchableOpacity>
              )}
            />
          </View>
        </Modal>
      </View>
    );
  }

  return (
    <View style={styles.authContainer}>
      <Text style={styles.title}>🎯 HITLIST</Text>
      <Text style={styles.subtitle}>Upload Photo</Text>
      
      {photoUri && (
        <Image source={{ uri: photoUri }} style={styles.photoPreview} />
      )}
      
      <TouchableOpacity style={styles.photoButton} onPress={selectPhoto}>
        <Text style={styles.photoButtonText}>
          {photoUri ? '📷 Change Photo' : '📷 Select Photo'}
        </Text>
      </TouchableOpacity>

      {photoUri && (
        <TouchableOpacity 
          style={[styles.button, loading && styles.buttonDisabled]} 
          onPress={handleCompleteSignup}
          disabled={loading}
        >
          <Text style={styles.buttonText}>
            {loading ? 'CREATING ACCOUNT...' : 'CREATE ACCOUNT'}
          </Text>
        </TouchableOpacity>
      )}
    </View>
  );
}

// Unverified Screen Component
function UnverifiedScreen({ user, onAuth }) {
  const [loading, setLoading] = useState(false);

  const checkVerificationStatus = async () => {
    setLoading(true);
    try {
      const { data: userData } = await supabase
        .from('users')
        .select('*')
        .eq('id', user.id)
        .single();
      
      if (userData) {
        onAuth(userData);
      }
    } catch (error) {
      console.error('Error checking verification:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={[styles.container, styles.centered]}>
      <Text style={styles.unverifiedTitle}>⏳ PENDING VERIFICATION</Text>
      <Text style={styles.unverifiedText}>
        Your account is awaiting approval.
      </Text>
      <TouchableOpacity 
        style={[styles.button, loading && styles.buttonDisabled]}
        onPress={checkVerificationStatus}
        disabled={loading}
      >
        <Text style={styles.buttonText}>
          {loading ? 'CHECKING...' : 'CHECK STATUS'}
        </Text>
      </TouchableOpacity>
      <TouchableOpacity 
        style={styles.signOutButton}
        onPress={async () => {
          await supabase.auth.signOut();
          onAuth(null);
        }}
      >
        <Text style={styles.signOutText}>Sign Out</Text>
      </TouchableOpacity>
    </View>
  );
}

// Compass Screen Component
function CompassScreen({ user }) {
  const [location, setLocation] = useState(null);
  const [heading, setHeading] = useState(0);
  const [target, setTarget] = useState(null);
  const [distance, setDistance] = useState(null);
  const [bearing, setBearing] = useState(null);
  const [shieldActive, setShieldActive] = useState(false);

  useEffect(() => {
    const initializeCompass = async () => {
      await requestLocationPermission();
      startMagnetometer();
      await fetchTarget();
      checkShieldStatus();
    };

    initializeCompass();

    return () => {
      Magnetometer.removeAllListeners();
    };
  }, []);

  const requestLocationPermission = async () => {
    const { status } = await Location.requestForegroundPermissionsAsync();
    if (status === 'granted') {
      startLocationTracking();
    }
  };

  const startLocationTracking = async () => {
    try {
      await Location.watchPositionAsync(
        {
          accuracy: Location.Accuracy.High,
          timeInterval: 1000,
          distanceInterval: 1,
        },
        (location) => {
          setLocation(location.coords);
          updateUserLocation(location.coords);
        }
      );
    } catch (error) {
      console.error('Location error:', error);
    }
  };

  const updateUserLocation = async (coords) => {
    try {
      await supabase
        .from('users')
        .update({
          last_lat: coords.latitude,
          last_lng: coords.longitude,
        })
        .eq('id', user.id);
    } catch (error) {
      console.error('Error updating location:', error);
    }
  };

  const startMagnetometer = () => {
    Magnetometer.setUpdateInterval(100);
    Magnetometer.addListener((data) => {
      const { x, y } = data;
      const heading = Math.atan2(y, x) * (180 / Math.PI);
      setHeading(heading >= 0 ? heading : heading + 360);
    });
  };

  const fetchTarget = async () => {
    if (!user.target_id) {
      await assignRandomTarget();
      return;
    }

    try {
      const { data: targetData } = await supabase
        .from('users')
        .select('*')
        .eq('id', user.target_id)
        .single();

      if (targetData) {
        setTarget(targetData);
      } else {
        await assignRandomTarget();
      }
    } catch (error) {
      console.error('Error fetching target:', error);
      await assignRandomTarget();
    }
  };

  const assignRandomTarget = async () => {
    try {
      const { data: players } = await supabase
        .from('users')
        .select('*')
        .eq('server_id', user.server_id)
        .eq('is_alive', true)
        .neq('id', user.id);

      if (players && players.length > 0) {
        const randomTarget = players[Math.floor(Math.random() * players.length)];
        
        await supabase
          .from('users')
          .update({ target_id: randomTarget.id })
          .eq('id', user.id);

        setTarget(randomTarget);
      }
    } catch (error) {
      console.error('Error assigning target:', error);
    }
  };

  const checkShieldStatus = () => {
    if (user.shield_until && new Date(user.shield_until) > new Date()) {
      setShieldActive(true);
    }
  };

  useEffect(() => {
    if (location && target && target.last_lat && target.last_lng) {
      const dist = calculateDistance(
        location.latitude,
        location.longitude,
        target.last_lat,
        target.last_lng
      );
      const bear = calculateBearing(
        location.latitude,
        location.longitude,
        target.last_lat,
        target.last_lng
      );

      setDistance(dist);
      setBearing(bear);
    }
  }, [location, target]);

  const compassRotation = bearing !== null ? bearing - heading : 0;
  const isInRange = distance !== null && distance <= 1609; // 1 mile

  return (
    <View style={styles.compassContainer}>
      <Text style={styles.screenTitle}>🧭 HUNT MODE</Text>
      
      {shieldActive && (
        <View style={styles.shieldIndicator}>
          <Text style={styles.shieldText}>🛡️ SHIELD ACTIVE</Text>
        </View>
      )}

      <View style={styles.compassCircle}>
        <View style={styles.compassCenter}>
          <Text style={styles.northText}>N</Text>
        </View>
        
        {target && isInRange && (
          <Animated.View
            style={[
              styles.compassArrow,
              {
                transform: [{ rotate: `${compassRotation}deg` }],
              },
            ]}
          >
            <Text style={styles.arrowText}>⬆️</Text>
          </Animated.View>
        )}
      </View>

      {target ? (
        <View style={styles.targetInfo}>
          <Text style={styles.targetName}>Target: {target.name}</Text>
          {distance !== null && (
            <Text style={styles.targetDistance}>
              {distance > 1609 
                ? `${(distance / 1609).toFixed(1)} miles away` 
                : `${Math.round(distance)} meters away`
              }
            </Text>
          )}
        </View>
      ) : (
        <View style={styles.targetInfo}>
          <Text style={styles.noTargetText}>No target assigned</Text>
        </View>
      )}

      {!isInRange && distance !== null && (
        <Text style={styles.outOfRangeText}>
          Target is {(distance / 1609).toFixed(1)} miles away - get closer!
        </Text>
      )}
    </View>
  );
}

// Action Screen Component
function ActionScreen({ user, setUser }) {
  const [location, setLocation] = useState(null);
  const [target, setTarget] = useState(null);
  const [distance, setDistance] = useState(null);
  const [loading, setLoading] = useState(false);
  const [shieldActive, setShieldActive] = useState(false);
  const [shieldTimeLeft, setShieldTimeLeft] = useState(0);

  useEffect(() => {
    const initializeAction = async () => {
      await requestLocationPermission();
      await fetchTarget();
      checkShieldStatus();
    };

    initializeAction();

    const interval = setInterval(() => {
      checkShieldStatus();
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const requestLocationPermission = async () => {
    const { status } = await Location.requestForegroundPermissionsAsync();
    if (status === 'granted') {
      startLocationTracking();
    }
  };

  const startLocationTracking = async () => {
    try {
      await Location.watchPositionAsync(
        {
          accuracy: Location.Accuracy.High,
          timeInterval: 1000,
          distanceInterval: 1,
        },
        (location) => {
          setLocation(location.coords);
          updateUserLocation(location.coords);
        }
      );
    } catch (error) {
      console.error('Location error:', error);
    }
  };

  const updateUserLocation = async (coords) => {
    try {
      await supabase
        .from('users')
        .update({
          last_lat: coords.latitude,
          last_lng: coords.longitude,
        })
        .eq('id', user.id);
    } catch (error) {
      console.error('Error updating location:', error);
    }
  };

  const fetchTarget = async () => {
    if (!user.target_id) return;

    try {
      const { data: targetData } = await supabase
        .from('users')
        .select('*')
        .eq('id', user.target_id)
        .single();

      if (targetData) {
        setTarget(targetData);
      }
    } catch (error) {
      console.error('Error fetching target:', error);
    }
  };

  const checkShieldStatus = () => {
    if (user.shield_until && new Date(user.shield_until) > new Date()) {
      setShieldActive(true);
      const timeLeft = Math.ceil((new Date(user.shield_until) - new Date()) / 1000);
      setShieldTimeLeft(timeLeft);
    } else {
      setShieldActive(false);
      setShieldTimeLeft(0);
    }
  };

  useEffect(() => {
    if (location && target && target.last_lat && target.last_lng) {
      const dist = calculateDistance(
        location.latitude,
        location.longitude,
        target.last_lat,
        target.last_lng
      );
      setDistance(dist);
    }
  }, [location, target]);

  const handleKill = async () => {
    if (!target || !location) {
      Alert.alert('Error', 'Target or location not available');
      return;
    }

    if (distance > 1) { // 1 meter = ~3 feet
      Alert.alert('Too Far!', 'You must be within 3 feet of your target to eliminate them.');
      return;
    }

    // Check if target has shield
    if (target.shield_until && new Date(target.shield_until) > new Date()) {
      Alert.alert(
        'Shield Active!',
        'Your target has an active shield. You have been eliminated instead!',
        [
          {
            text: 'OK',
            onPress: async () => {
              await handlePlayerDeath();
            },
          },
        ]
      );
      return;
    }

    setLoading(true);
    try {
      // Record the kill
      await supabase.from('kills').insert({
        killer_id: user.id,
        victim_id: target.id,
        timestamp: new Date().toISOString(),
      });

      // Update killer stats and assign new target
      await supabase
        .from('users')
        .update({
          kills: user.kills + 1,
          points: user.points + 1,
          target_id: target.target_id,
        })
        .eq('id', user.id);

      // Mark victim as dead and reset their stats
      await supabase
        .from('users')
        .update({
          is_alive: false,
          points: 0,
          target_id: null,
          shield_until: null,
        })
        .eq('id', target.id);

      // Reassign victim a new target after respawn
      await respawnPlayer(target.id);

      Alert.alert('🎯 KILL CONFIRMED!', `You eliminated ${target.name}!`);
      
      // Refresh user data
      const { data: updatedUser } = await supabase
        .from('users')
        .select('*')
        .eq('id', user.id)
        .single();
      
      if (updatedUser) {
        setUser(updatedUser);
      }

      // Fetch new target
      await fetchTarget();

    } catch (error) {
      console.error('Kill error:', error);
      Alert.alert('Error', 'Failed to process kill');
    } finally {
      setLoading(false);
    }
  };

  const respawnPlayer = async (playerId) => {
    try {
      // Get available targets
      const { data: availableTargets } = await supabase
        .from('users')
        .select('*')
        .eq('server_id', user.server_id)
        .eq('is_alive', true)
        .neq('id', playerId);

      if (availableTargets && availableTargets.length > 0) {
        const randomTarget = availableTargets[Math.floor(Math.random() * availableTargets.length)];
        
        // Respawn the player
        await supabase
          .from('users')
          .update({
            is_alive: true,
            target_id: randomTarget.id,
          })
          .eq('id', playerId);
      }
    } catch (error) {
      console.error('Respawn error:', error);
    }
  };

  const handlePlayerDeath = async () => {
    try {
      await supabase
        .from('users')
        .update({
          is_alive: false,
          points: 0,
          target_id: null,
          shield_until: null,
        })
        .eq('id', user.id);

      // Respawn after death
      await respawnPlayer(user.id);

      // Refresh user data
      const { data: updatedUser } = await supabase
        .from('users')
        .select('*')
        .eq('id', user.id)
        .single();
      
      if (updatedUser) {
        setUser(updatedUser);
      }

    } catch (error) {
      console.error('Death handling error:', error);
    }
  };

  const activateShield = async () => {
    if (shieldActive) {
      Alert.alert('Shield Active', 'Your shield is already active');
      return;
    }

    setLoading(true);
    try {
      const shieldUntil = new Date();
      shieldUntil.setMinutes(shieldUntil.getMinutes() + 10); // 10 minutes

      await supabase
        .from('users')
        .update({
          shield_until: shieldUntil.toISOString(),
        })
        .eq('id', user.id);

      // Update user state
      const updatedUser = { ...user, shield_until: shieldUntil.toISOString() };
      setUser(updatedUser);
      
      setShieldActive(true);
      Alert.alert('🛡️ Shield Activated!', 'You are protected for 10 minutes');

    } catch (error) {
      console.error('Shield activation error:', error);
      Alert.alert('Error', 'Failed to activate shield');
    } finally {
      setLoading(false);
    }
  };

  const canKill = distance !== null && distance <= 1 && target && !shieldActive;

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.screenTitle}>⚡ ACTION CENTER</Text>

      <View style={styles.statsCard}>
        <Text style={styles.statLabel}>Your Stats</Text>
        <Text style={styles.statValue}>Kills: {user.kills}</Text>
        <Text style={styles.statValue}>Points: {user.points}</Text>
        <Text style={styles.statValue}>Status: {user.is_alive ? '🟢 Alive' : '🔴 Dead'}</Text>
      </View>

      {shieldActive && (
        <View style={styles.shieldCard}>
          <Text style={styles.shieldTitle}>🛡️ SHIELD ACTIVE</Text>
          <Text style={styles.shieldTime}>
            {Math.floor(shieldTimeLeft / 60)}:{(shieldTimeLeft % 60).toString().padStart(2, '0')} remaining
          </Text>
        </View>
      )}

      {target && (
        <View style={styles.targetCard}>
          <Text style={styles.targetTitle}>🎯 Current Target</Text>
          <Text style={styles.targetName}>{target.name}</Text>
          {distance !== null && (
            <Text style={styles.targetDistance}>
              {distance <= 1 ? `${(distance * 3.28084).toFixed(1)} feet away` : `${distance.toFixed(0)}m away`}
            </Text>
          )}
        </View>
      )}

      <View style={styles.actionButtons}>
        <TouchableOpacity
          style={[
            styles.killButton,
            (!canKill || loading) && styles.buttonDisabled,
          ]}
          onPress={handleKill}
          disabled={!canKill || loading}
        >
          <Text style={styles.killButtonText}>
            {loading ? 'PROCESSING...' : '💀 ELIMINATE'}
          </Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[
            styles.shieldButton,
            (shieldActive || loading) && styles.buttonDisabled,
          ]}
          onPress={activateShield}
          disabled={shieldActive || loading}
        >
          <Text style={styles.shieldButtonText}>
            {shieldActive ? '🛡️ ACTIVE' : '🛡️ SHIELD'}
          </Text>
        </TouchableOpacity>
      </View>

      <View style={styles.rulesCard}>
        <Text style={styles.rulesTitle}>📋 Rules</Text>
        <Text style={styles.rulesText}>• Must be within 3 feet to eliminate</Text>
        <Text style={styles.rulesText}>• Shield lasts 10 minutes</Text>
        <Text style={styles.rulesText}>• Attacking shielded target = death</Text>
        <Text style={styles.rulesText}>• Death resets points to 0</Text>
      </View>
    </ScrollView>
  );
}

// Leaderboard Screen Component
function LeaderboardScreen({ user }) {
  const [players, setPlayers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState('kills');

  useEffect(() => {
    fetchLeaderboard();
  }, [sortBy]);

  const fetchLeaderboard = async () => {
    setLoading(true);
    try {
      const { data: playersData } = await supabase
        .from('users')
        .select('id, name, kills, points, is_alive')
        .eq('server_id', user.server_id)
        .eq('verified', true)
        .order(sortBy, { ascending: false });

      if (playersData) {
        setPlayers(playersData);
      }
    } catch (error) {
      console.error('Leaderboard fetch error:', error);
    } finally {
      setLoading(false);
    }
  };

  const renderPlayer = ({ item, index }) => (
    <View style={[
      styles.playerCard,
      item.id === user.id && styles.currentPlayerCard
    ]}>
      <Text style={styles.playerRank}>#{index + 1}</Text>
      <View style={styles.playerInfo}>
        <Text style={styles.playerName}>
          {item.name} {item.id === user.id && '(You)'}
        </Text>
        <Text style={styles.playerStats}>
          {item.kills} kills • {item.points} points
        </Text>
      </View>
      <Text style={styles.playerStatus}>
        {item.is_alive ? '🟢' : '🔴'}
      </Text>
    </View>
  );

  return (
    <View style={styles.container}>
      <Text style={styles.screenTitle}>🏆 LEADERBOARD</Text>

      <View style={styles.sortButtons}>
        <TouchableOpacity
          style={[styles.sortButton, sortBy === 'kills' && styles.sortButtonActive]}
          onPress={() => setSortBy('kills')}
        >
          <Text style={[styles.sortButtonText, sortBy === 'kills' && styles.sortButtonTextActive]}>
            By Kills
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.sortButton, sortBy === 'points' && styles.sortButtonActive]}
          onPress={() => setSortBy('points')}
        >
          <Text style={[styles.sortButtonText, sortBy === 'points' && styles.sortButtonTextActive]}>
            By Points
          </Text>
        </TouchableOpacity>
      </View>

      {loading ? (
        <View style={styles.centered}>
          <ActivityIndicator size="large" color="#00ff00" />
        </View>
      ) : (
        <FlatList
          data={players}
          keyExtractor={(item) => item.id}
          renderItem={renderPlayer}
          showsVerticalScrollIndicator={false}
          contentContainerStyle={styles.leaderboardList}
        />
      )}
    </View>
  );
}

// Chat Screen Component
function ChatScreen({ user }) {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [chatType, setChatType] = useState('local');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchMessages();
    
    const subscription = supabase
      .channel('chat_changes')
      .on(
        'postgres_changes',
        {
          event: '*',
          schema: 'public',
          table: 'chats',
        },
        () => {
          fetchMessages();
        }
      )
      .subscribe();

    return () => {
      supabase.removeChannel(subscription);
    };
  }, [chatType]);

  const fetchMessages = async () => {
    try {
      let query = supabase
        .from('chats')
        .select(`
          id,
          message,
          timestamp,
          type,
          sender:sender_id(name)
        `)
        .eq('type', chatType)
        .order('timestamp', { ascending: false })
        .limit(50);

      if (chatType === 'local') {
        query = query.eq('server_id', user.server_id);
      }

      const { data: messagesData } = await query;

      if (messagesData) {
        setMessages(messagesData.reverse());
      }
    } catch (error) {
      console.error('Messages fetch error:', error);
    }
  };

  const sendMessage = async () => {
    if (!newMessage.trim()) return;

    setLoading(true);
    try {
      await supabase.from('chats').insert({
        sender_id: user.id,
        message: newMessage.trim(),
        type: chatType,
        server_id: chatType === 'local' ? user.server_id : null,
        timestamp: new Date().toISOString(),
      });

      setNewMessage('');
      await fetchMessages();
    } catch (error) {
      console.error('Send message error:', error);
      Alert.alert('Error', 'Failed to send message');
    } finally {
      setLoading(false);
    }
  };

  const renderMessage = ({ item }) => (
    <View style={[
      styles.messageCard,
      item.sender_id === user.id && styles.ownMessage
    ]}>
      <Text style={styles.messageSender}>{item.sender?.name || 'Unknown'}</Text>
      <Text style={styles.messageText}>{item.message}</Text>
      <Text style={styles.messageTime}>
        {new Date(item.timestamp).toLocaleTimeString()}
      </Text>
    </View>
  );

  return (
    <View style={styles.chatContainer}>
      <Text style={styles.screenTitle}>💬 CHAT</Text>

      <View style={styles.chatTabs}>
        <TouchableOpacity
          style={[styles.chatTab, chatType === 'local' && styles.chatTabActive]}
          onPress={() => setChatType('local')}
        >
          <Text style={[styles.chatTabText, chatType === 'local' && styles.chatTabTextActive]}>
            Local
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.chatTab, chatType === 'mod' && styles.chatTabActive]}
          onPress={() => setChatType('mod')}
        >
          <Text style={[styles.chatTabText, chatType === 'mod' && styles.chatTabTextActive]}>
            Moderator
          </Text>
        </TouchableOpacity>
      </View>

      <FlatList
        data={messages}
        keyExtractor={(item) => item.id}
        renderItem={renderMessage}
        style={styles.messagesList}
        showsVerticalScrollIndicator={false}
      />

      <View style={styles.messageInput}>
        <TextInput
          style={styles.messageTextInput}
          placeholder="Type a message..."
          placeholderTextColor="#666"
          value={newMessage}
          onChangeText={setNewMessage}
          multiline
        />
        <TouchableOpacity
          style={[styles.sendButton, loading && styles.buttonDisabled]}
          onPress={sendMessage}
          disabled={loading || !newMessage.trim()}
        >
          <Text style={styles.sendButtonText}>Send</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

// Moderator Screen Component
function ModeratorScreen({ user }) {
  const [pendingUsers, setPendingUsers] = useState([]);
  const [allUsers, setAllUsers] = useState([]);
  const [tab, setTab] = useState('pending');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchPendingUsers();
    fetchAllUsers();
  }, []);

  const fetchPendingUsers = async () => {
    try {
      let query = supabase
        .from('users')
        .select('*')
        .eq('verified', false);

      if (user.email !== SUPER_ADMIN_EMAIL) {
        query = query.neq('role', 'pending_mod');
      }

      const { data } = await query;
      if (data) setPendingUsers(data);
    } catch (error) {
      console.error('Fetch pending users error:', error);
    }
  };

  const fetchAllUsers = async () => {
    try {
      const { data } = await supabase
        .from('users')
        .select('*')
        .order('created_at', { ascending: false });

      if (data) setAllUsers(data);
    } catch (error) {
      console.error('Fetch all users error:', error);
    }
  };

  const approveUser = async (userId, userRole) => {
    setLoading(true);
    try {
      const updates = { verified: true };
      
      if (userRole === 'pending_mod' && user.email === SUPER_ADMIN_EMAIL) {
        updates.role = 'moderator';
      }

      await supabase
        .from('users')
        .update(updates)
        .eq('id', userId);

      Alert.alert('Success', 'User approved successfully');
      await fetchPendingUsers();
      await fetchAllUsers();
    } catch (error) {
      console.error('Approve user error:', error);
      Alert.alert('Error', 'Failed to approve user');
    } finally {
      setLoading(false);
    }
  };

  const rejectUser = async (userId) => {
    Alert.alert(
      'Reject User',
      'Are you sure you want to reject this user?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Reject',
          style: 'destructive',
          onPress: async () => {
            try {
              await supabase
                .from('users')
                .delete()
                .eq('id', userId);

              Alert.alert('Success', 'User rejected');
              await fetchPendingUsers();
              await fetchAllUsers();
            } catch (error) {
              console.error('Reject user error:', error);
              Alert.alert('Error', 'Failed to reject user');
            }
          },
        },
      ]
    );
  };

  const banUser = async (userId, banned) => {
    try {
      await supabase
        .from('users')
        .update({ banned })
        .eq('id', userId);

      Alert.alert('Success', `User ${banned ? 'banned' : 'unbanned'} successfully`);
      await fetchAllUsers();
    } catch (error) {
      console.error('Ban user error:', error);
      Alert.alert('Error', `Failed to ${banned ? 'ban' : 'unban'} user`);
    }
  };

  const timeoutUser = async (userId, minutes) => {
    try {
      const timeoutUntil = new Date();
      timeoutUntil.setMinutes(timeoutUntil.getMinutes() + minutes);

      await supabase
        .from('users')
        .update({ timeout_until: timeoutUntil.toISOString() })
        .eq('id', userId);

      Alert.alert('Success', `User timed out for ${minutes} minutes`);
      await fetchAllUsers();
    } catch (error) {
      console.error('Timeout user error:', error);
      Alert.alert('Error', 'Failed to timeout user');
    }
  };

  const renderPendingUser = ({ item }) => (
    <View style={styles.moderatorCard}>
      <Text style={styles.moderatorUserName}>{item.name}</Text>
      <Text style={styles.moderatorUserEmail}>{item.email}</Text>
      <Text style={styles.moderatorUserRole}>Role: {item.role}</Text>
      
      {item.photo_url && (
        <Image source={{ uri: item.photo_url }} style={styles.moderatorPhoto} />
      )}
      
      <View style={styles.moderatorActions}>
        <TouchableOpacity
          style={styles.approveButton}
          onPress={() => approveUser(item.id, item.role)}
          disabled={loading}
        >
          <Text style={styles.approveButtonText}>Approve</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.rejectButton}
          onPress={() => rejectUser(item.id)}
          disabled={loading}
        >
          <Text style={styles.rejectButtonText}>Reject</Text>
        </TouchableOpacity>
      </View>
    </View>
  );

  const renderUser = ({ item }) => (
    <View style={styles.moderatorCard}>
      <Text style={styles.moderatorUserName}>{item.name}</Text>
      <Text style={styles.moderatorUserEmail}>{item.email}</Text>
      <Text style={styles.moderatorUserRole}>
        Role: {item.role} | Status: {item.banned ? '🚫 Banned' : item.verified ? '✅ Verified' : '⏳ Pending'}
      </Text>
      <Text style={styles.moderatorUserStats}>
        Kills: {item.kills} | Points: {item.points} | {item.is_alive ? '🟢 Alive' : '🔴 Dead'}
      </Text>
      
      <View style={styles.moderatorActions}>
        <TouchableOpacity
          style={item.banned ? styles.unbanButton : styles.banButton}
          onPress={() => banUser(item.id, !item.banned)}
        >
          <Text style={styles.banButtonText}>
            {item.banned ? 'Unban' : 'Ban'}
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.timeoutButton}
          onPress={() => {
            Alert.alert(
              'Timeout User',
              'Select timeout duration:',
              [
                { text: 'Cancel', style: 'cancel' },
                { text: '10 min', onPress: () => timeoutUser(item.id, 10) },
                { text: '1 hour', onPress: () => timeoutUser(item.id, 60) },
                { text: '24 hours', onPress: () => timeoutUser(item.id, 1440) },
              ]
            );
          }}
        >
          <Text style={styles.timeoutButtonText}>Timeout</Text>
        </TouchableOpacity>
      </View>
    </View>
  );

  return (
    <View style={styles.container}>
      <Text style={styles.screenTitle}>🛡️ MODERATOR PANEL</Text>

      <View style={styles.moderatorTabs}>
        <TouchableOpacity
          style={[styles.moderatorTab, tab === 'pending' && styles.moderatorTabActive]}
          onPress={() => setTab('pending')}
        >
          <Text style={[styles.moderatorTabText, tab === 'pending' && styles.moderatorTabTextActive]}>
            Pending ({pendingUsers.length})
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.moderatorTab, tab === 'all' && styles.moderatorTabActive]}
          onPress={() => setTab('all')}
        >
          <Text style={[styles.moderatorTabText, tab === 'all' && styles.moderatorTabTextActive]}>
            All Users
          </Text>
        </TouchableOpacity>
      </View>

      <FlatList
        data={tab === 'pending' ? pendingUsers : allUsers}
        keyExtractor={(item) => item.id}
        renderItem={tab === 'pending' ? renderPendingUser : renderUser}
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.moderatorList}
      />
    </View>
  );
}

// Complete Styles
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0a0a0a',
  },
  centered: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    color: '#00ff00',
    fontSize: 16,
    marginTop: 10,
  },
  // Auth Screen Styles
  authContainer: {
    flex: 1,
    backgroundColor: '#0a0a0a',
    padding: 20,
    justifyContent: 'center',
  },
  title: {
    fontSize: 42,
    fontWeight: 'bold',
    color: '#00ff00',
    textAlign: 'center',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 18,
    color: '#fff',
    textAlign: 'center',
    marginBottom: 30,
  },
  input: {
    backgroundColor: '#1a1a1a',
    borderWidth: 1,
    borderColor: '#333',
    color: '#fff',
    fontSize: 16,
    padding: 15,
    borderRadius: 10,
    marginBottom: 15,
  },
  button: {
    backgroundColor: '#00ff00',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
    marginBottom: 15,
  },
  buttonDisabled: {
    backgroundColor: '#004400',
  },
  buttonText: {
    color: '#000',
    fontSize: 16,
    fontWeight: 'bold',
  },
  linkText: {
    color: '#00ff00',
    textAlign: 'center',
    fontSize: 16,
  },
  accountTypeSelector: {
    flexDirection: 'row',
    marginBottom: 20,
  },
  typeButton: {
    flex: 1,
    padding: 15,
    borderWidth: 1,
    borderColor: '#333',
    alignItems: 'center',
    marginHorizontal: 5,
    borderRadius: 10,
  },
  typeButtonActive: {
    backgroundColor: '#00ff00',
    borderColor: '#00ff00',
  },
  typeButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  typeButtonTextActive: {
    color: '#000',
  },
  schoolSelector: {
    backgroundColor: '#1a1a1a',
    borderWidth: 1,
    borderColor: '#333',
    padding: 15,
    borderRadius: 10,
    marginBottom: 15,
  },
  schoolSelectorText: {
    color: '#fff',
    fontSize: 16,
  },
  photoButton: {
    backgroundColor: '#333',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
    marginBottom: 15,
  },
  photoButtonText: {
    color: '#fff',
    fontSize: 16,
  },
  photoPreview: {
    width: 200,
    height: 150,
    borderRadius: 10,
    alignSelf: 'center',
    marginBottom: 15,
  },
  // Modal Styles
  modalContainer: {
    flex: 1,
    backgroundColor: '#0a0a0a',
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#333',
  },
  modalTitle: {
    color: '#00ff00',
    fontSize: 20,
    fontWeight: 'bold',
  },
  closeButton: {
    color: '#fff',
    fontSize: 24,
  },
  schoolItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#222',
  },
  schoolName: {
    color: '#fff',
    fontSize: 16,
  },
  schoolState: {
    color: '#666',
    fontSize: 14,
  },
  // Status Screen Styles
  bannedTitle: {
    color: '#ff0000',
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 20,
  },
  bannedText: {
    color: '#fff',
    fontSize: 16,
    textAlign: 'center',
    marginBottom: 30,
  },
  timeoutTitle: {
    color: '#ffaa00',
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 20,
  },
  timeoutText: {
    color: '#fff',
    fontSize: 16,
    textAlign: 'center',
    marginBottom: 30,
  },
  unverifiedTitle: {
    color: '#ffaa00',
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 20,
  },
  unverifiedText: {
    color: '#fff',
    fontSize: 16,
    textAlign: 'center',
    marginBottom: 30,
  },
  signOutButton: {
    marginTop: 20,
  },
  signOutText: {
    color: '#666',
    textAlign: 'center',
    fontSize: 16,
  },
  // Navigation Styles
  tabBar: {
    backgroundColor: '#1a1a1a',
    borderTopColor: '#333',
  },
  header: {
    backgroundColor: '#0a0a0a',
  },
  headerTitle: {
    color: '#00ff00',
    fontSize: 18,
    fontWeight: 'bold',
  },
  screenTitle: {
    color: '#00ff00',
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    padding: 20,
  },
  // Compass Screen Styles
  compassContainer: {
    flex: 1,
    backgroundColor: '#0a0a0a',
    alignItems: 'center',
  },
  shieldIndicator: {
    backgroundColor: '#004400',
    padding: 10,
    borderRadius: 20,
    marginBottom: 20,
  },
  shieldText: {
    color: '#00ff00',
    fontWeight: 'bold',
  },
  compassCircle: {
    width: 250,
    height: 250,
    borderRadius: 125,
    borderWidth: 3,
    borderColor: '#00ff00',
    backgroundColor: '#1a1a1a',
    justifyContent: 'center',
    alignItems: 'center',
    position: 'relative',
  },
  compassCenter: {
    position: 'absolute',
    top: 10,
  },
  northText: {
    color: '#00ff00',
    fontSize: 24,
    fontWeight: 'bold',
  },
  compassArrow: {
    position: 'absolute',
  },
  arrowText: {
    fontSize: 30,
  },
  targetInfo: {
    alignItems: 'center',
    marginTop: 30,
  },
  targetName: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  targetDistance: {
    color: '#00ff00',
    fontSize: 16,
    marginTop: 5,
  },
  noTargetText: {
    color: '#666',
    fontSize: 16,
  },
  outOfRangeText: {
    color: '#ffaa00',
    fontSize: 14,
    textAlign: 'center',
    marginTop: 20,
    paddingHorizontal: 20,
  },
  // Action Screen Styles
  statsCard: {
    backgroundColor: '#1a1a1a',
    margin: 15,
    padding: 20,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#333',
  },
  statLabel: {
    color: '#00ff00',
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  statValue: {
    color: '#fff',
    fontSize: 14,
    marginBottom: 5,
  },
  shieldCard: {
    backgroundColor: '#004400',
    margin: 15,
    padding: 20,
    borderRadius: 10,
    alignItems: 'center',
  },
  shieldTitle: {
    color: '#00ff00',
    fontSize: 18,
    fontWeight: 'bold',
  },
  shieldTime: {
    color: '#00ff00',
    fontSize: 14,
    marginTop: 5,
  },
  targetCard: {
    backgroundColor: '#1a1a1a',
    margin: 15,
    padding: 20,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#333',
  },
  targetTitle: {
    color: '#00ff00',
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  actionButtons: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    margin: 15,
  },
  killButton: {
    backgroundColor: '#ff0000',
    padding: 15,
    borderRadius: 10,
    flex: 0.45,
    alignItems: 'center',
  },
  killButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  shieldButton: {
    backgroundColor: '#00ff00',
    padding: 15,
    borderRadius: 10,
    flex: 0.45,
    alignItems: 'center',
  },
  shieldButtonText: {
    color: '#000',
    fontWeight: 'bold',
  },
  rulesCard: {
    backgroundColor: '#1a1a1a',
    margin: 15,
    padding: 20,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#333',
  },
  rulesTitle: {
    color: '#00ff00',
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  rulesText: {
    color: '#fff',
    fontSize: 14,
    marginBottom: 5,
  },
  // Leaderboard Styles
  sortButtons: {
    flexDirection: 'row',
    margin: 15,
  },
  sortButton: {
    flex: 1,
    padding: 12,
    backgroundColor: '#1a1a1a',
    borderColor: '#333',
    borderWidth: 1,
    alignItems: 'center',
    marginHorizontal: 5,
    borderRadius: 8,
  },
  sortButtonActive: {
    backgroundColor: '#00ff00',
  },
  sortButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  sortButtonTextActive: {
    color: '#000',
  },
  leaderboardList: {
    paddingHorizontal: 15,
  },
  playerCard: {
    backgroundColor: '#1a1a1a',
    padding: 15,
    borderRadius: 10,
    marginBottom: 10,
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#333',
  },
  currentPlayerCard: {
    borderColor: '#00ff00',
    backgroundColor: '#002200',
  },
  playerRank: {
    color: '#00ff00',
    fontSize: 18,
    fontWeight: 'bold',
    width: 50,
  },
  playerInfo: {
    flex: 1,
  },
  playerName: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  playerStats: {
    color: '#666',
    fontSize: 14,
  },
  playerStatus: {
    fontSize: 20,
  },
  // Chat Styles
  chatContainer: {
    flex: 1,
    backgroundColor: '#0a0a0a',
  },
  chatTabs: {
    flexDirection: 'row',
    margin: 15,
  },
  chatTab: {
    flex: 1,
    padding: 12,
    backgroundColor: '#1a1a1a',
    borderColor: '#333',
    borderWidth: 1,
    alignItems: 'center',
    marginHorizontal: 5,
    borderRadius: 8,
  },
  chatTabActive: {
    backgroundColor: '#00ff00',
  },
  chatTabText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  chatTabTextActive: {
    color: '#000',
  },
  messagesList: {
    flex: 1,
    paddingHorizontal: 15,
  },
  messageCard: {
    backgroundColor: '#1a1a1a',
    padding: 12,
    borderRadius: 8,
    marginBottom: 8,
    alignSelf: 'flex-start',
    maxWidth: '80%',
  },
  ownMessage: {
    backgroundColor: '#004400',
    alignSelf: 'flex-end',
  },
  messageSender: {
    color: '#00ff00',
    fontSize: 12,
    fontWeight: 'bold',
  },
  messageText: {
    color: '#fff',
    fontSize: 16,
    marginVertical: 4,
  },
  messageTime: {
    color: '#666',
    fontSize: 10,
  },
  messageInput: {
    flexDirection: 'row',
    padding: 15,
    borderTopWidth: 1,
    borderTopColor: '#333',
  },
  messageTextInput: {
    flex: 1,
    backgroundColor: '#1a1a1a',
    color: '#fff',
    padding: 10,
    borderRadius: 8,
    marginRight: 10,
    maxHeight: 100,
  },
  sendButton: {
    backgroundColor: '#00ff00',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 8,
    justifyContent: 'center',
  },
  sendButtonText: {
    color: '#000',
    fontWeight: 'bold',
  },
  // Moderator Styles
  moderatorTabs: {
    flexDirection: 'row',
    margin: 15,
  },
  moderatorTab: {
    flex: 1,
    padding: 12,
    backgroundColor: '#1a1a1a',
    borderColor: '#333',
    borderWidth: 1,
    alignItems: 'center',
    marginHorizontal: 5,
    borderRadius: 8,
  },
  moderatorTabActive: {
    backgroundColor: '#00ff00',
  },
  moderatorTabText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  moderatorTabTextActive: {
    color: '#000',
  },
  moderatorList: {
    paddingHorizontal: 15,
  },
  moderatorCard: {
    backgroundColor: '#1a1a1a',
    padding: 15,
    borderRadius: 10,
    marginBottom: 10,
    borderWidth: 1,
    borderColor: '#333',
  },
  moderatorUserName: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  moderatorUserEmail: {
    color: '#666',
    fontSize: 14,
  },
  moderatorUserRole: {
    color: '#00ff00',
    fontSize: 14,
    marginTop: 5,
  },
  moderatorUserStats: {
    color: '#666',
    fontSize: 12,
    marginTop: 5,
  },
  moderatorPhoto: {
    width: 60,
    height: 45,
    borderRadius: 8,
    marginVertical: 10,
  },
  moderatorActions: {
    flexDirection: 'row',
    marginTop: 10,
  },
  approveButton: {
    backgroundColor: '#00ff00',
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 6,
    marginRight: 10,
  },
  approveButtonText: {
    color: '#000',
    fontWeight: 'bold',
  },
  rejectButton: {
    backgroundColor: '#ff0000',
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 6,
  },
  rejectButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  banButton: {
    backgroundColor: '#ff0000',
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 6,
    marginRight: 10,
  },
  unbanButton: {
    backgroundColor: '#00ff00',
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 6,
    marginRight: 10,
  },
  banButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  timeoutButton: {
    backgroundColor: '#ffaa00',
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 6,
  },
  timeoutButtonText: {
    color: '#000',
    fontWeight: 'bold',
  },
});
