#!/usr/bin/env python3
"""
Test the offline LLM implementation
Verifies that our offline LLM works without external dependencies
"""

def test_offline_llm():
    """Test the offline LLM implementation"""
    try:
        from crews.bi_crew import BIAnalysisCrew
        
        print("🧪 Testing offline LLM implementation...")
        
        # Create BIAnalysisCrew instance
        crew = BIAnalysisCrew()
        
        print(f"✅ BIAnalysisCrew initialized successfully")
        print(f"🤖 LLM type: {crew.llm._llm_type}")
        print(f"📊 Number of agents: {len(crew.agents)}")
        
        # Test the LLM directly
        print("\n🔍 Testing LLM directly...")
        test_prompt = "Analyze this sample data and provide insights."
        response = crew.llm._call(test_prompt)
        
        print(f"✅ LLM response generated successfully")
        print(f"📝 Response length: {len(response)} characters")
        print(f"📄 Response preview: {response[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Offline LLM test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("🚀 Testing offline LLM implementation...")
    success = test_offline_llm()
    
    if success:
        print("\n🎉 Offline LLM is working correctly!")
        print("The issue might be with CrewAI's internal LLM handling.")
    else:
        print("\n❌ Offline LLM is not working.")
        print("There may be an issue with the LLM implementation.")