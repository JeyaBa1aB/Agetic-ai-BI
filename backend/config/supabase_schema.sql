-- Supabase schema for Multi-Agent BI Assistant
-- Run this SQL in your Supabase SQL editor to create the required tables

-- Create analysis_sessions table
CREATE TABLE IF NOT EXISTS analysis_sessions (
    id BIGSERIAL PRIMARY KEY,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    query TEXT,
    csv_data TEXT,
    status VARCHAR(50) DEFAULT 'initialized',
    user_id VARCHAR(255) DEFAULT 'anonymous',
    metadata JSONB DEFAULT '{}',
    agents_status JSONB DEFAULT '{}',
    results JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create agent_results table
CREATE TABLE IF NOT EXISTS agent_results (
    id BIGSERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    agent_id VARCHAR(255) NOT NULL,
    result JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (session_id) REFERENCES analysis_sessions(session_id) ON DELETE CASCADE
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_analysis_sessions_session_id ON analysis_sessions(session_id);
CREATE INDEX IF NOT EXISTS idx_analysis_sessions_created_at ON analysis_sessions(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_agent_results_session_id ON agent_results(session_id);
CREATE INDEX IF NOT EXISTS idx_agent_results_created_at ON agent_results(created_at);

-- Enable Row Level Security (RLS) for better security
ALTER TABLE analysis_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_results ENABLE ROW LEVEL SECURITY;

-- Create policies for public access (adjust as needed for your security requirements)
CREATE POLICY "Allow all operations on analysis_sessions" ON analysis_sessions
    FOR ALL USING (true);

CREATE POLICY "Allow all operations on agent_results" ON agent_results
    FOR ALL USING (true);

-- Create a function to automatically update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at on analysis_sessions
CREATE TRIGGER update_analysis_sessions_updated_at 
    BEFORE UPDATE ON analysis_sessions 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();