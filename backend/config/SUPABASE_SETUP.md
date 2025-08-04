# Supabase Setup Guide

This guide will help you set up Supabase for the Multi-Agent BI Assistant project.

## Prerequisites

1. Create a Supabase account at [supabase.com](https://supabase.com)
2. Create a new project in your Supabase dashboard

## Configuration Steps

### 1. Get Your Supabase Credentials

From your Supabase project dashboard:

1. Go to **Settings** → **API**
2. Copy your **Project URL** 
3. Copy your **anon/public** key
4. Copy your **service_role** key (optional, for admin operations)

### 2. Update Environment Variables

Update your `backend/.env` file with your Supabase credentials:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key-here
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here
```

### 3. Create Database Tables

1. Go to your Supabase dashboard
2. Navigate to **SQL Editor**
3. Copy and paste the contents of `backend/config/supabase_schema.sql`
4. Click **Run** to execute the SQL

This will create:
- `analysis_sessions` table for storing analysis sessions
- `agent_results` table for storing individual agent results
- Appropriate indexes for performance
- Row Level Security policies
- Automatic timestamp updates

### 4. Test Your Connection

Run the Supabase test script to verify everything is working:

```bash
cd backend
python config/test_supabase.py
```

You should see output indicating successful connection and basic operations.

## Database Schema

### analysis_sessions
- `id`: Primary key (auto-generated)
- `session_id`: Unique session identifier
- `query`: User's analysis query
- `csv_data`: Uploaded CSV data
- `status`: Current analysis status
- `user_id`: User identifier
- `metadata`: Additional session metadata (JSON)
- `agents_status`: Status of each agent (JSON)
- `results`: Analysis results (JSON)
- `created_at`: Session creation timestamp
- `updated_at`: Last update timestamp

### agent_results
- `id`: Primary key (auto-generated)
- `session_id`: Reference to analysis session
- `agent_id`: Identifier of the agent
- `result`: Agent's analysis result (JSON)
- `created_at`: Result creation timestamp

## Security Notes

- The current setup uses permissive RLS policies for development
- For production, implement proper user authentication and restrict policies
- Consider using the service role key only for server-side operations
- The anon key should be used for client-side operations

## Troubleshooting

### Connection Issues
- Verify your SUPABASE_URL and SUPABASE_KEY are correct
- Check that your Supabase project is active
- Ensure your network allows connections to Supabase

### Table Creation Issues
- Make sure you have the necessary permissions
- Check the SQL Editor for any error messages
- Verify the schema matches your requirements

### Test Script Failures
- Ensure all environment variables are set correctly
- Check that the tables were created successfully
- Review the error messages for specific issues