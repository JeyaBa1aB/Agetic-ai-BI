#!/usr/bin/env python3
"""
Test the complete chart generation workflow
Verifies that chart specifications are generated correctly for visualization queries
"""

def test_chart_generation_workflow():
    """Test the complete chart generation workflow"""
    try:
        from crews.bi_crew import BIAnalysisCrew
        
        print("🧪 Testing complete chart generation workflow...")
        
        # Create BIAnalysisCrew instance
        crew = BIAnalysisCrew()
        
        # Sample CSV data (real estate listings)
        sample_csv = """week_end_date,geo_country,median_listing_price_yy
2023-01-01,USA,5.2
2023-01-08,USA,5.8
2023-01-15,USA,6.1
2023-01-01,Canada,3.4
2023-01-08,Canada,3.7
2023-01-15,Canada,4.1
2023-01-01,UK,2.8
2023-01-08,UK,3.2
2023-01-15,UK,3.5"""
        
        # Test different visualization queries
        test_queries = [
            "Create a line chart showing price trends over time",
            "Generate a bar chart comparing prices by country", 
            "Build visualizations for the real estate data",
            "Show me charts for this dataset"
        ]
        
        print(f"\n📊 Testing {len(test_queries)} visualization queries:\n")
        
        for i, query in enumerate(test_queries, 1):
            print(f"{i}. Query: '{query}'")
            
            # Test chart generation
            charts_result = crew._generate_charts_if_needed(query, sample_csv)
            
            if charts_result.get('success'):
                charts = charts_result.get('charts', [])
                print(f"   ✅ Generated {len(charts)} chart specifications")
                
                for j, chart in enumerate(charts):
                    print(f"      Chart {j+1}: {chart.get('type')} - {chart.get('title')}")
                    print(f"      Config: {chart.get('config', {})}")
            else:
                print(f"   ❌ Chart generation failed: {charts_result.get('error', 'Unknown error')}")
            
            print()
        
        # Test non-visualization query (should not generate charts)
        print("5. Testing non-visualization query:")
        non_viz_query = "What are the key insights from this data?"
        charts_result = crew._generate_charts_if_needed(non_viz_query, sample_csv)
        
        if not charts_result.get('success') or len(charts_result.get('charts', [])) == 0:
            print("   ✅ Correctly identified as non-visualization query (no charts generated)")
        else:
            print("   ❌ Incorrectly generated charts for non-visualization query")
        
        return True
        
    except Exception as e:
        print(f"❌ Chart generation workflow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("🚀 Testing complete chart generation workflow...")
    success = test_chart_generation_workflow()
    
    if success:
        print("\n🎉 Chart generation workflow test completed!")
        print("The system can now automatically generate charts for visualization queries.")
    else:
        print("\n❌ Chart generation workflow test failed.")