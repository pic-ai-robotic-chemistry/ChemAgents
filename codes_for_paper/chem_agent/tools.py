from langchain_core.tools import tool
# from langchain_community.tools.tavily_search import TavilySearchResults

# tool_Tavily = TavilySearchResults(max_results=3)

# @tool
# def multiply(a: int, b: int) -> int:
#     """Multiply two numbers."""
#     return a * b

@tool
def query_literature_database(str):
    """query literature data base"""
    str = str.lower()
    print("query-str:",str)
    if "oer" in str or "oxygen evolution reaction" in str:
        index = [1,2,3,4]
    else:
        index = [5,6,7]
    return index

@tool
def literature_mining(str,index):
    """literature mining"""
    print("mining-str:",str,index)
    str = str.lower()
    if "oer" in str or "oxygen evolution reaction" in str:
        if index == [1,2,3,4]:
            element=[1,2]
    elif "sod" in str:
        if index == [5,6,7]:
            element=[3,4]
    print("element",element)
    return element

@tool
def query_experiment_template_library(str):
    """query experiment template library"""
    str = str.lower()
    if "oer" in str or "oxygen evolution reaction" in str:
        template = '''1. Retrieve the racks from the sample rack station.
2. Use the liquid station to add 5g of cobalt acetate solution.
3. Use the liquid station to add 5g of iron acetate solution.
4. Use the liquid station to add 5g phthalic acid solution.
5. Use the magnetic stirring station to stir the mixture at 500 rpm for 24 hours at 25 ℃.
6. Use the centrifuge station to centrifuge at 5000 rpm for 3 minutes.
7. Use the aspiration station to aspirate the liquid above the sample after centrifugation.
8. Use the liquid station to add 8 g Nafion solution.
9. Use the electrocatalytic station to perform electrochemical tests. '''
    else:
        template = 0
    print("query-str:",str)
    return template

@tool
def query_station_list(str):
    """query experiment station list"""
    #station_list=['solid station,can add solid to the val','liquid,can add liquid to the val']
    station_list=''' 1. The sample rack station for retrieving and returning the sample rack;
2. The liquid station for adding various liquid reagents, the parameters that can be set are mass in grams;
3. The solid station for adding various solid reagents, the parameters that can be set are mass in grams;
4. The magnetic stirring station, used for mixing and stirring while heating various reagents, the parameters that can be set are time and temperature, where the unit of time is second and the unit of temperature is Celsius;
5. The centrifuge station for separating the components of a mixture of liquid and solid particles, or a mixture of liquid and liquid. The parameters that can be set are time and rotational speed, where time is in seconds and rotational speed is in r/min;
6. The aspiration station for aspirating the waste liquid above the sample after centrifugation;
7. The drying station for heating samples, the parameters that can be set are drying time in seconds;
8. The ultrasonic cleaning station for cleaning samples or accelerating reactions, the parameters that can be set are cleaning time in seconds;
9. The encapsulation station, used to encapsulate the reaction vessel under vacuum;
10. The photocatalytic station for performing photocatalytic tests, where the parameter that can be set is the photocatalytic time in seconds;
11. The gas chromatography station, used to test the sample gas chromatography;
12. The Raman station for testing sample Raman spectra;
13. The infrared spectroscopy station, used to test the infrared spectrum of the sample;
14. The UV spectroscopy station for testing sample UV spectra;
15. The fluorescence spectroscopy station, used to test the sample fluorescence spectrum.
16. The XRD station, used to test the sample X-ray diffraction spectrum; 
17. The LIBS station for testing sample laser induced breakdown spectra;
18. The electrocatalytic station for performing electrocatalytic tests. 
19. The calcination station for calcination and heating of samples.
20. The shaker station for mixing, dissolution, reaction, and other operations.
21. The drop-cast station for dropping the sample onto the test strip.
22. The spin-coating station for preparing thin film with dropped sample solution.'''

    return station_list
