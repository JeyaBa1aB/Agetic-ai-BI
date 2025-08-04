/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Custom agent color scheme
        agent: {
          // Data Intelligence Team
          'data-analyst': '#3B82F6',      // Blue
          'data-processor': '#06B6D4',    // Cyan
          'pattern-detector': '#8B5CF6',  // Purple

          // Visualization Team
          'chart-specialist': '#10B981',   // Emerald
          'dashboard-designer': '#F59E0B', // Amber

          // Business Intelligence Team
          'business-strategist': '#EF4444', // Red
          'market-analyst': '#F97316',      // Orange

          // Reporting Team
          'executive-reporter': '#6366F1',  // Indigo

          // Master Orchestrator
          'master-orchestrator': '#1F2937', // Gray-800
        },
        // Status colors
        status: {
          'ready': '#10B981',      // Green
          'working': '#F59E0B',    // Amber
          'completed': '#3B82F6',  // Blue
          'error': '#EF4444',      // Red
          'idle': '#6B7280',       // Gray
        },
        // Background colors
        background: {
          'primary': '#F9FAFB',    // Gray-50
          'secondary': '#F3F4F6',  // Gray-100
          'card': '#FFFFFF',       // White
          'dark': '#111827',       // Gray-900
        }
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'bounce-slow': 'bounce 2s infinite',
        'spin-slow': 'spin 3s linear infinite',
      },
      fontFamily: {
        'sans': ['Inter', 'system-ui', 'sans-serif'],
        'mono': ['JetBrains Mono', 'monospace'],
      },
      boxShadow: {
        'agent': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'agent-hover': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
      }
    },
  },
  plugins: [],
}