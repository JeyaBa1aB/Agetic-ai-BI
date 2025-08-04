/**
 * Supabase client configuration
 * Handles database operations and real-time subscriptions
 */
import { createClient } from '@supabase/supabase-js';

// Supabase configuration
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.warn('⚠️ Supabase configuration missing. Some features may not work.');
}

// Create Supabase client
export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    persistSession: false, // We're not using auth for now
  },
  realtime: {
    params: {
      eventsPerSecond: 10,
    },
  },
});

// Database operations
export const supabaseService = {
  // Analysis sessions
  async getAnalysisSessions(limit = 10) {
    try {
      const { data, error } = await supabase
        .from('analysis_sessions')
        .select('*')
        .order('created_at', { ascending: false })
        .limit(limit);

      if (error) throw error;
      return data;
    } catch (error) {
      console.error('Error fetching analysis sessions:', error);
      throw error;
    }
  },

  async getAnalysisSession(sessionId) {
    try {
      const { data, error } = await supabase
        .from('analysis_sessions')
        .select('*')
        .eq('session_id', sessionId)
        .single();

      if (error) throw error;
      return data;
    } catch (error) {
      console.error('Error fetching analysis session:', error);
      throw error;
    }
  },

  async createAnalysisSession(sessionData) {
    try {
      const { data, error } = await supabase
        .from('analysis_sessions')
        .insert([sessionData])
        .select()
        .single();

      if (error) throw error;
      return data;
    } catch (error) {
      console.error('Error creating analysis session:', error);
      throw error;
    }
  },

  async updateAnalysisSession(sessionId, updates) {
    try {
      const { data, error } = await supabase
        .from('analysis_sessions')
        .update(updates)
        .eq('session_id', sessionId)
        .select()
        .single();

      if (error) throw error;
      return data;
    } catch (error) {
      console.error('Error updating analysis session:', error);
      throw error;
    }
  },

  async deleteAnalysisSession(sessionId) {
    try {
      const { error } = await supabase
        .from('analysis_sessions')
        .delete()
        .eq('session_id', sessionId);

      if (error) throw error;
      return true;
    } catch (error) {
      console.error('Error deleting analysis session:', error);
      throw error;
    }
  },

  // Agent results
  async getAgentResults(sessionId) {
    try {
      const { data, error } = await supabase
        .from('agent_results')
        .select('*')
        .eq('session_id', sessionId)
        .order('created_at', { ascending: true });

      if (error) throw error;
      return data;
    } catch (error) {
      console.error('Error fetching agent results:', error);
      throw error;
    }
  },

  async createAgentResult(resultData) {
    try {
      const { data, error } = await supabase
        .from('agent_results')
        .insert([resultData])
        .select()
        .single();

      if (error) throw error;
      return data;
    } catch (error) {
      console.error('Error creating agent result:', error);
      throw error;
    }
  },

  // Real-time subscriptions
  subscribeToAnalysisSessions(callback) {
    const subscription = supabase
      .channel('analysis_sessions_changes')
      .on('postgres_changes', 
        { 
          event: '*', 
          schema: 'public', 
          table: 'analysis_sessions' 
        }, 
        callback
      )
      .subscribe();

    return subscription;
  },

  subscribeToAgentResults(sessionId, callback) {
    const subscription = supabase
      .channel(`agent_results_${sessionId}`)
      .on('postgres_changes', 
        { 
          event: '*', 
          schema: 'public', 
          table: 'agent_results',
          filter: `session_id=eq.${sessionId}`
        }, 
        callback
      )
      .subscribe();

    return subscription;
  },

  // Unsubscribe from real-time updates
  unsubscribe(subscription) {
    if (subscription) {
      supabase.removeChannel(subscription);
    }
  },

  // Test connection
  async testConnection() {
    try {
      const { data, error } = await supabase
        .from('analysis_sessions')
        .select('count')
        .limit(1);

      if (error) throw error;
      console.log('✅ Supabase connection test successful');
      return true;
    } catch (error) {
      console.error('❌ Supabase connection test failed:', error);
      return false;
    }
  }
};

export default supabase;