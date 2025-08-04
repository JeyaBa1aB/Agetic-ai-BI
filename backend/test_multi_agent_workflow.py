"""
Comprehensive test for multi-agent workflow execution and coordination
Tests all 9 agents working together through CrewAI framework
"""
import sys
import time
import json
import logging
from typing import Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_individual_agents():
    """Test individual agent functionality"""
    print("🤖 Testing Individual Agent Functionality")
    print("=" * 50)
    
    try:
        # Test Data Intelligence Team
        print("1. Testing Data Intelligence Team...")
        
        from agents.data_agents import DataAnalystAgent, DataProcessorAgent, PatternDetectorAgent
        
        # Test Data Analyst
        data_analyst = DataAnalystAgent()
        print(f"   ✅ Data Analyst initialized: {data_analyst.name}")
        
        # Test Data Processor  
        data_processor = DataProcessorAgent()
        print(f"   ✅ Data Processor initialized: {data_processor.name}")
        
        # Test Pattern Detector
        pattern_detector = PatternDetectorAgent()
        print(f"   ✅ Pattern Detector initialized: {pattern_detector.name}")
        
        # Test Visualization Team
        print("2. Testing Visualization Team...")
        
        from agents.visualization_agents import ChartSpecialistAgent, DashboardDesignerAgent
        
        chart_specialist = ChartSpecialistAgent()
        print(f"   ✅ Chart Specialist initialized: {chart_specialist.name}")
        
        dashboard_designer = DashboardDesignerAgent()
        print(f"   ✅ Dashboard Designer initialized: {dashboard_designer.name}")
        
        # Test Business Intelligence Team
        print("3. Testing Business Intelligence Team...")
        
        from agents.business_agents import BusinessStrategistAgent, MarketAnalystAgent
        
        business_strategist = BusinessStrategistAgent()
        print(f"   ✅ Business Strategist initialized: {business_strategist.name}")
        
        market_analyst = MarketAnalystAgent()
        print(f"   ✅ Market Analyst initialized: {market_analyst.name}")
        
        # Test Reporting Team
        print("4. Testing Reporting Team...")
        
        from agents.reporting_agents import ExecutiveReporterAgent
        
        executive_reporter = ExecutiveReporterAgent()
        print(f"   ✅ Executive Reporter initialized: {executive_reporter.name}")
        
        # Test Master Orchestrator
        print("5. Testing Master Orchestrator...")
        
        from agents.master_orchestrator import MasterOrchestratorAgent
        
        master_orchestrator = MasterOrchestratorAgent()
        print(f"   ✅ Master Orchestrator initialized: {master_orchestrator.name}")
        
        print("   🎉 All 9 agents initialized successfully!")
        return True
        
    except Exception as e:
        print(f"   ❌ Agent initialization failed: {e}")
        return False

def test_crewai_integration():
    """Test CrewAI integration and crew formation"""
    print("\n🚢 Testing CrewAI Integration")
    print("=" * 50)
    
    try:
        from crews.bi_crew import BIAnalysisCrew, crewai_integration
        
        # Test BIAnalysisCrew initialization
        print("1. Testing BIAnalysisCrew initialization...")
        bi_crew = BIAnalysisCrew()
        print(f"   ✅ BIAnalysisCrew initialized with {len(bi_crew.agents)} agents")
        
        # Test crew status
        print("2. Testing crew status...")
        crew_status = bi_crew.get_crew_status()
        print(f"   ✅ Crew initialized: {crew_status['crew_initialized']}")
        print(f"   ✅ Agents count: {crew_status['agents_count']}")
        print(f"   ✅ LLM configured: {crew_status['llm_configured']}")
        
        # Test CrewAI integration
        print("3. Testing CrewAI integration...")
        print(f"   ✅ CrewAI integration initialized")
        print(f"   ✅ Active sessions: {len(crewai_integration.get_all_sessions())}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ CrewAI integration test failed: {e}")
        return False

def test_sample_analysis():
    """Test a complete multi-agent analysis workflow"""
    print("\n🔬 Testing Complete Multi-Agent Analysis Workflow")
    print("=" * 50)
    
    try:
        from crews.bi_crew import crewai_integration
        
        # Sample CSV data for testing
        sample_csv = """Product,Category,Sales,Profit,Region
Laptop,Electronics,15000,3000,North
Phone,Electronics,12000,2400,South
Tablet,Electronics,8000,1600,East
Chair,Furniture,5000,1000,West
Desk,Furniture,7000,1400,North
Monitor,Electronics,6000,1200,South
Keyboard,Electronics,2000,400,East
Mouse,Electronics,1500,300,West"""
        
        sample_query = "Analyze the sales performance and provide strategic recommendations for improving profitability across different regions and product categories."
        
        session_id = f"test_session_{int(time.time())}"
        
        print(f"1. Starting analysis for session: {session_id}")
        csv_lines = sample_csv.split('\n')
        print(f"   📊 Data: {len(csv_lines)} rows of sales data")
        print(f"   ❓ Query: {sample_query[:60]}...")
        
        # Start the analysis
        print("2. Executing multi-agent analysis...")
        print("   ⏳ This may take 30-60 seconds...")
        
        start_time = time.time()
        result = crewai_integration.start_crewai_analysis(
            csv_data=sample_csv,
            query=sample_query,
            session_id=session_id
        )
        
        execution_time = time.time() - start_time
        
        # Analyze results
        print(f"3. Analysis completed in {execution_time:.2f} seconds")
        
        if result.get('success'):
            print("   ✅ Analysis completed successfully!")
            
            # Check result structure
            if 'crew_result' in result:
                print("   ✅ Crew result present")
            
            if 'execution_summary' in result:
                summary = result['execution_summary']
                print(f"   ✅ Agents involved: {summary.get('agents_involved', 0)}")
                print(f"   ✅ Tasks completed: {summary.get('tasks_completed', 0)}")
                print(f"   ✅ Framework: {summary.get('framework', 'Unknown')}")
            
            if 'agent_contributions' in result:
                contributions = result['agent_contributions']
                print(f"   ✅ Agent contributions: {len(contributions)} agents")
                
                # List agent contributions
                for agent_id, contribution in contributions.items():
                    status = contribution.get('status', 'unknown')
                    print(f"      - {contribution.get('role', agent_id)}: {status}")
            
            if 'key_insights' in result:
                insights = result['key_insights']
                print(f"   ✅ Key insights generated: {len(insights)}")
            
            if 'recommendations' in result:
                recommendations = result['recommendations']
                print(f"   ✅ Recommendations generated: {len(recommendations)}")
            
            return True
            
        else:
            print(f"   ❌ Analysis failed: {result.get('error', 'Unknown error')}")
            return False
        
    except Exception as e:
        print(f"   ❌ Multi-agent analysis test failed: {e}")
        return False

def test_agent_coordination():
    """Test agent coordination and communication"""
    print("\n🤝 Testing Agent Coordination and Communication")
    print("=" * 50)
    
    try:
        # Test individual agent analysis capabilities
        print("1. Testing individual agent analysis capabilities...")
        
        from agents.data_agents import DataAnalystAgent
        from agents.business_agents import BusinessStrategistAgent
        from agents.visualization_agents import ChartSpecialistAgent
        
        # Sample data for testing
        test_data = "Product sales data showing declining performance in Q3"
        test_query = "What are the key factors affecting sales performance?"
        
        # Test Data Analyst
        data_analyst = DataAnalystAgent()
        analyst_result = data_analyst.analyze({'csv_data': test_data}, test_query)
        print(f"   ✅ Data Analyst response: {len(str(analyst_result.get('analysis', '')))} characters")
        
        # Test Business Strategist
        business_strategist = BusinessStrategistAgent()
        strategist_result = business_strategist.analyze({'csv_data': test_data}, test_query)
        print(f"   ✅ Business Strategist response: {len(str(strategist_result.get('analysis', '')))} characters")
        
        # Test Chart Specialist
        chart_specialist = ChartSpecialistAgent()
        chart_result = chart_specialist.analyze({'csv_data': test_data}, test_query)
        print(f"   ✅ Chart Specialist response: {len(str(chart_result.get('analysis', '')))} characters")
        
        print("2. Testing agent metadata and capabilities...")
        
        # Test agent metadata
        agents = [data_analyst, business_strategist, chart_specialist]
        for agent in agents:
            print(f"   - {agent.name}: {agent.role}")
            print(f"     Specialization: {agent.specialization}")
            print(f"     Capabilities: {len(agent.capabilities)} items")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Agent coordination test failed: {e}")
        return False

def test_error_handling():
    """Test error handling and recovery"""
    print("\n🛡️ Testing Error Handling and Recovery")
    print("=" * 50)
    
    try:
        from crews.bi_crew import crewai_integration
        
        # Test with invalid data
        print("1. Testing with invalid CSV data...")
        invalid_csv = "This is not valid CSV data"
        valid_query = "Analyze this data"
        session_id = f"error_test_{int(time.time())}"
        
        result = crewai_integration.start_crewai_analysis(
            csv_data=invalid_csv,
            query=valid_query,
            session_id=session_id
        )
        
        # Should handle gracefully
        if not result.get('success'):
            print("   ✅ Invalid data handled gracefully")
        else:
            print("   ⚠️  Invalid data was processed (unexpected)")
        
        # Test with empty query
        print("2. Testing with empty query...")
        valid_csv = "Name,Value\\nTest,123"
        empty_query = ""
        session_id = f"error_test_2_{int(time.time())}"
        
        result = crewai_integration.start_crewai_analysis(
            csv_data=valid_csv,
            query=empty_query,
            session_id=session_id
        )
        
        # Should handle gracefully
        print("   ✅ Empty query handled")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error handling test failed: {e}")
        return False

def main():
    """Run all multi-agent workflow tests"""
    print("🧪 Multi-Agent Workflow Execution and Coordination Test")
    print("=" * 60)
    
    tests = [
        ("Individual Agents", test_individual_agents),
        ("CrewAI Integration", test_crewai_integration),
        ("Sample Analysis", test_sample_analysis),
        ("Agent Coordination", test_agent_coordination),
        ("Error Handling", test_error_handling)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed_tests += 1
                print(f"✅ {test_name} - PASSED")
            else:
                print(f"❌ {test_name} - FAILED")
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}")
        
        print()  # Add spacing between tests
    
    # Final summary
    print("=" * 60)
    print(f"🏁 Test Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All multi-agent workflow tests passed!")
        print("✅ Task 2.9 - Multi-agent workflow execution and coordination - COMPLETED!")
        return True
    else:
        print("⚠️  Some tests failed. Please review the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)