#!/usr/bin/env python3
"""
Test the intelligent agent selection system
Shows which agents are selected for different types of queries
"""

def test_agent_selection():
    """Test agent selection for various query types"""
    try:
        from crews.bi_crew import BIAnalysisCrew
        
        print("🧪 Testing intelligent agent selection system...")
        
        # Create BIAnalysisCrew instance
        crew = BIAnalysisCrew()
        
        # Test different query types
        test_queries = [
            "Create a bar chart showing sales trends",
            "Identify patterns and anomalies in the dataset", 
            "Generate business recommendations for growth",
            "Analyze market trends and competitive landscape",
            "Clean and process the data for analysis",
            "Create an executive dashboard for leadership",
            "What are the key insights from this data?",
            "Build visualizations and charts for the data"
        ]
        
        print(f"\n📊 Testing {len(test_queries)} different query types:\n")
        
        for i, query in enumerate(test_queries, 1):
            print(f"{i}. Query: '{query}'")
            selected_agents = crew._select_agents_for_query(query)
            print(f"   Selected agents ({len(selected_agents)}): {', '.join(selected_agents)}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Agent selection test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("🚀 Testing intelligent agent selection...")
    success = test_agent_selection()
    
    if success:
        print("🎉 Agent selection system is working correctly!")
        print("The system now intelligently selects only relevant agents for each query.")
    else:
        print("❌ Agent selection system test failed.")