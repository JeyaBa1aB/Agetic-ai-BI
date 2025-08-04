/**
 * Workflow Progress component for multi-stage analysis progress tracking
 * Shows the current stage and overall progress of the analysis
 */
import React, { useState, useEffect } from 'react';
import { CheckCircle, Clock, Play, AlertCircle, TrendingUp } from 'lucide-react';

const WorkflowProgress = ({ sessionId, websocket }) => {
  const [currentStage, setCurrentStage] = useState('initialization');
  const [overallProgress, setOverallProgress] = useState(0);
  const [stageProgress, setStageProgress] = useState({});
  const [completedTasks, setCompletedTasks] = useState([]);
  const [startTime, setStartTime] = useState(null);
  const [estimatedTimeRemaining, setEstimatedTimeRemaining] = useState(null);

  // Workflow stages configuration
  const workflowStages = [
    {
      id: 'initialization',
      name: 'Initialization',
      description: 'Setting up analysis session and preparing agents',
      icon: Play,
      estimatedDuration: 5
    },
    {
      id: 'data_intelligence',
      name: 'Data Intelligence',
      description: 'Analyzing data quality, patterns, and statistical insights',
      icon: TrendingUp,
      estimatedDuration: 30
    },
    {
      id: 'visualization_planning',
      name: 'Visualization Planning',
      description: 'Designing charts and dashboard layouts',
      icon: TrendingUp,
      estimatedDuration: 20
    },
    {
      id: 'business_analysis',
      name: 'Business Analysis',
      description: 'Strategic insights and market analysis',
      icon: TrendingUp,
      estimatedDuration: 25
    },
    {
      id: 'executive_reporting',
      name: 'Executive Reporting',
      description: 'Generating comprehensive reports and summaries',
      icon: TrendingUp,
      estimatedDuration: 15
    },
    {
      id: 'synthesis',
      name: 'Synthesis',
      description: 'Combining all agent results into final analysis',
      icon: CheckCircle,
      estimatedDuration: 10
    }
  ];

  // Initialize progress tracking
  useEffect(() => {
    if (sessionId) {
      setStartTime(Date.now());
      setCurrentStage('initialization');
      setOverallProgress(0);
      setStageProgress({});
      setCompletedTasks([]);
      setEstimatedTimeRemaining(null);
    }
  }, [sessionId]);

  // Listen for workflow updates
  useEffect(() => {
    if (!websocket || !sessionId) return;

    const handleWorkflowStageUpdate = (data) => {
      if (data.session_id === sessionId) {
        setCurrentStage(data.stage);
        console.log('Workflow stage updated:', data);
      }
    };

    const handleWorkflowProgressUpdate = (data) => {
      if (data.session_id === sessionId) {
        setOverallProgress(data.progress || 0);
        
        if (data.stage) {
          setStageProgress(prev => ({
            ...prev,
            [data.stage]: data.progress || 0
          }));
        }

        // Update estimated time remaining
        if (startTime && data.progress > 0) {
          const elapsed = Date.now() - startTime;
          const totalEstimated = (elapsed / data.progress) * 100;
          const remaining = totalEstimated - elapsed;
          setEstimatedTimeRemaining(Math.max(0, remaining));
        }

        console.log('Workflow progress updated:', data);
      }
    };

    const handleTaskStarted = (data) => {
      if (data.session_id === sessionId) {
        console.log('Task started:', data);
      }
    };

    const handleTaskCompleted = (data) => {
      if (data.session_id === sessionId) {
        setCompletedTasks(prev => [...prev, {
          taskIndex: data.task_index,
          agentName: data.agent_name,
          timestamp: Date.now()
        }]);
        console.log('Task completed:', data);
      }
    };

    const handleAnalysisStarted = (data) => {
      if (data.session_id === sessionId) {
        setCurrentStage('data_intelligence');
        setOverallProgress(10);
      }
    };

    const handleAnalysisCompleted = (data) => {
      if (data.session_id === sessionId) {
        setCurrentStage('synthesis');
        setOverallProgress(100);
        setEstimatedTimeRemaining(0);
      }
    };

    // Subscribe to events
    websocket.subscribe('workflow_stage_update', handleWorkflowStageUpdate);
    websocket.subscribe('workflow_progress_update', handleWorkflowProgressUpdate);
    websocket.subscribe('task_started', handleTaskStarted);
    websocket.subscribe('task_completed', handleTaskCompleted);
    websocket.subscribe('analysis_started', handleAnalysisStarted);
    websocket.subscribe('analysis_completed', handleAnalysisCompleted);

    return () => {
      websocket.unsubscribe('workflow_stage_update', handleWorkflowStageUpdate);
      websocket.unsubscribe('workflow_progress_update', handleWorkflowProgressUpdate);
      websocket.unsubscribe('task_started', handleTaskStarted);
      websocket.unsubscribe('task_completed', handleTaskCompleted);
      websocket.unsubscribe('analysis_started', handleAnalysisStarted);
      websocket.unsubscribe('analysis_completed', handleAnalysisCompleted);
    };
  }, [websocket, sessionId, startTime]);

  // Get stage status
  const getStageStatus = (stage) => {
    const stageIndex = workflowStages.findIndex(s => s.id === stage.id);
    const currentIndex = workflowStages.findIndex(s => s.id === currentStage);

    if (stageIndex < currentIndex) return 'completed';
    if (stageIndex === currentIndex) return 'active';
    return 'pending';
  };

  // Format time
  const formatTime = (milliseconds) => {
    const seconds = Math.floor(milliseconds / 1000);
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;

    if (minutes > 0) {
      return `${minutes}m ${remainingSeconds}s`;
    }
    return `${remainingSeconds}s`;
  };

  // Get elapsed time
  const getElapsedTime = () => {
    if (!startTime) return 0;
    return Date.now() - startTime;
  };

  return (
    <div className="space-y-6">
      
      {/* Overall Progress */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="font-medium text-gray-900">
            Analysis Progress
          </h3>
          <div className="text-sm text-gray-600">
            {Math.round(overallProgress)}%
          </div>
        </div>

        {/* Progress Bar */}
        <div className="progress-bar h-3">
          <div 
            className="progress-fill h-3 transition-all duration-500 ease-out"
            style={{ width: `${overallProgress}%` }}
          ></div>
        </div>

        {/* Time Information */}
        <div className="flex items-center justify-between text-sm text-gray-600">
          <div className="flex items-center space-x-4">
            {startTime && (
              <span>
                ⏱️ Elapsed: {formatTime(getElapsedTime())}
              </span>
            )}
            {estimatedTimeRemaining && estimatedTimeRemaining > 0 && (
              <span>
                ⏳ Remaining: ~{formatTime(estimatedTimeRemaining)}
              </span>
            )}
          </div>
          
          <div>
            {completedTasks.length > 0 && (
              <span>
                ✅ {completedTasks.length} tasks completed
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Stage Progress */}
      <div className="space-y-3">
        <h4 className="font-medium text-gray-900">
          Workflow Stages
        </h4>

        <div className="space-y-2">
          {workflowStages.map((stage, index) => {
            const status = getStageStatus(stage);
            const StageIcon = stage.icon;
            const progress = stageProgress[stage.id] || 0;

            return (
              <div
                key={stage.id}
                className={`p-3 rounded-lg border transition-all duration-200 ${
                  status === 'active'
                    ? 'bg-blue-50 border-blue-200'
                    : status === 'completed'
                    ? 'bg-green-50 border-green-200'
                    : 'bg-gray-50 border-gray-200'
                }`}
              >
                <div className="flex items-center space-x-3">
                  {/* Stage Icon */}
                  <div className={`p-2 rounded-full ${
                    status === 'active'
                      ? 'bg-blue-100 text-blue-600'
                      : status === 'completed'
                      ? 'bg-green-100 text-green-600'
                      : 'bg-gray-100 text-gray-400'
                  }`}>
                    {status === 'active' ? (
                      <StageIcon className="w-4 h-4 animate-pulse" />
                    ) : status === 'completed' ? (
                      <CheckCircle className="w-4 h-4" />
                    ) : (
                      <Clock className="w-4 h-4" />
                    )}
                  </div>

                  {/* Stage Info */}
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <h5 className={`font-medium ${
                        status === 'active'
                          ? 'text-blue-900'
                          : status === 'completed'
                          ? 'text-green-900'
                          : 'text-gray-700'
                      }`}>
                        {stage.name}
                      </h5>
                      
                      {status === 'active' && progress > 0 && (
                        <span className="text-sm text-blue-600 font-medium">
                          {Math.round(progress)}%
                        </span>
                      )}
                    </div>

                    <p className={`text-sm ${
                      status === 'active'
                        ? 'text-blue-700'
                        : status === 'completed'
                        ? 'text-green-700'
                        : 'text-gray-600'
                    }`}>
                      {stage.description}
                    </p>

                    {/* Stage Progress Bar */}
                    {status === 'active' && progress > 0 && (
                      <div className="mt-2">
                        <div className="w-full bg-blue-200 rounded-full h-1.5">
                          <div 
                            className="bg-blue-500 h-1.5 rounded-full transition-all duration-300"
                            style={{ width: `${progress}%` }}
                          ></div>
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Stage Number */}
                  <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-medium ${
                    status === 'active'
                      ? 'bg-blue-500 text-white'
                      : status === 'completed'
                      ? 'bg-green-500 text-white'
                      : 'bg-gray-300 text-gray-600'
                  }`}>
                    {index + 1}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Recent Task Completions */}
      {completedTasks.length > 0 && (
        <div className="space-y-3">
          <h4 className="font-medium text-gray-900">
            Recent Completions
          </h4>
          
          <div className="space-y-2 max-h-32 overflow-y-auto">
            {completedTasks.slice(-5).reverse().map((task, index) => (
              <div
                key={`${task.taskIndex}-${task.timestamp}`}
                className="flex items-center space-x-2 text-sm text-gray-600 p-2 bg-green-50 rounded border border-green-200"
              >
                <CheckCircle className="w-4 h-4 text-green-600" />
                <span className="flex-1">
                  {task.agentName} completed task {task.taskIndex + 1}
                </span>
                <span className="text-xs text-gray-500">
                  {new Date(task.timestamp).toLocaleTimeString()}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* No session message */}
      {!sessionId && (
        <div className="text-center p-6 text-gray-500">
          <Clock className="w-8 h-8 mx-auto mb-2 opacity-50" />
          <p className="text-sm">
            Start an analysis to track workflow progress
          </p>
        </div>
      )}
    </div>
  );
};

export default WorkflowProgress;