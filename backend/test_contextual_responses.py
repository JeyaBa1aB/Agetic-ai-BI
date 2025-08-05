#!/usr/bin/env python3
"""
Test the enhanced contextual LLM responses
Verifies that different query types generate appropriate responses
"""

def test_contextual_responses():
    """Test contextual responses for different query types"""
    try:
        from crews.bi_crew import BIAnalysisCrew
        
        print("🧪 Testing enhanced contextual LLM responses...")
        
        # Create BIAnalysisCrew instance
        crew = BIAnalysisCrew()
        
        # Test different query types with sample prompts
        test_cases = [
            {
                'type': 'Chart/Visualization',
                'prompt': 'Create a bar chart showing sales trends over time. CSV Data: week_end_date,geo_country,median_listing_price_yy Query: "Create visualizations for the data"',
                'expected_keywords': ['Chart Types', 'Time Series', 'Geographic Heat Map', 'visualization']
            },
            {
                'type': 'Pattern Detection', 
                'prompt': 'Identify patterns and anomalies in the dataset. CSV Data: week_end_date,geo_country,median_listing_price_yy Query: "Find patterns in the data"',
                'expected_keywords': ['Temporal Trends', 'Geographic Variations', 'Anomaly Detection', 'patterns']
            },
            {
                'type': 'Business Strategy',
                'prompt': 'Generate business recommendations for growth. CSV Data: week_end_date,geo_country,median_listing_price_yy Query: "Provide business recommendations"',
                'expected_keywords': ['Strategic Opportunities', 'Market Expansion', 'Business Recommendations', 'Implementation Roadmap']
            },
            {
                'type': 'General Analysis',
                'prompt': 'What are the key insights from this data? CSV Data: week_end_date,geo_country,median_listing_price_yy Query: "Analyze the data"',
                'expected_keywords': ['Key Insights', 'Performance Trends', 'Geographic Variations', 'Actionable Recommendations']
            }
        ]
        
        print(f"\n📊 Testing {len(test_cases)} different response types:\n")
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"{i}. Testing {test_case['type']}:")
            print(f"   Prompt: {test_case['prompt'][:80]}...")
            
            # Get response from LLM
            response = crew.llm._call(test_case['prompt'])
            
            # Check if response contains expected keywords
            found_keywords = []
            for keyword in test_case['expected_keywords']:
                if keyword.lower() in response.lower():
                    found_keywords.append(keyword)
            
            print(f"   Response length: {len(response)} characters")
            print(f"   Found keywords: {found_keywords}")
            print(f"   Response preview: {response[:150]}...")
            
            # Check if this is the old generic response
            if "Data Analysis Summary" in response and "Key Findings:" in response and len(found_keywords) == 0:
                print(f"   ❌ Still using old generic response!")
            else:
                print(f"   ✅ Using enhanced contextual response!")
            
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Contextual response test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("🚀 Testing enhanced contextual LLM responses...")
    success = test_contextual_responses()
    
    if success:
        print("🎉 Contextual response system test completed!")
        print("Check the results above to see if enhanced responses are working.")
    else:
        print("❌ Contextual response system test failed.")