#
# All tools can be found here.
# Some of the customized tools related to local resources (Literature Database, Protocol Library, Model Library, Experimental Data) are accessed through internal networks. They need to be replaced with corresponding resources.
#

from langchain_core.tools import tool
# from langchain_community.tools.tavily_search import TavilySearchResults

# tool_Tavily = TavilySearchResults(max_results=3)

from literature_reader import LR
from experiment_designer import ED
from robot_operator import RO
from computation_performer import CP

# @tool
# def multiply(a: int, b: int) -> int:
#     """Multiply two numbers."""
#     return a * b

@tool
def query_literature_database(str):
    """query literature data base, `str` usually includes the name of the experiment that needs to be designed or the experiment object made or synthesize"""
    str = str.lower()
    # `LiteratureSearch` function requests access to the Literature Database and queries literature data, with results provided by the local Database. The Literature Database is temporarily not open for external access. It need to be replaced with corresponding resources.
    index = LiteratureSearch(str)
    return index

@tool
def literature_mining(str,index):
    """literature mining, `str` usually includes the name of the experiment that needs to be designed or the experiment object made or synthesize, `index` usually includes the index of relevant literature in the literature database"""
    str = str.lower()
    # `LiterateMine` function requests access to the Literature Database, retrieves literature based on the index, and uses customized NLP tool for data mining to obtain results. The Literature Database is temporarily not open for external access. It need to be replaced with corresponding resources.
    result = LiteratureMine(str,index)
    if "oer" in str or "oxygen evolution reaction" in str:
        result = result['element']
    return result

@tool
def query_experiment_template_library(str):
    """query experiment template library, `str` usually includes the name of the experiment that needs to be designed or the experiment object made or synthesize"""
    str = str.lower()
    # `ProtocolSearch` function requests access to the Protocol Library and queries procedural templates, with results provided by the local Library. The Protocol Library is temporarily not open for external access. It need to be replaced with corresponding resources.
    template = ProtocolSearch(str)
    return template

@tool
def query_station_list(str):
    """get the list of available automated stations"""
    station_list=''' 1. Sample rack station: For retrieving and returning sample racks.
2. Liquid station: For adding pre-configured liquid reagents (ten different reagents can be placed at the same time). Parameters that can be set are mass (g) and the type of liquid.
3. Solid station: For adding pre-filled solid reagents. Parameters that can be set are mass (g) and the type of solid.
4. Magnetic stirring station: For mixing and stirring different reagents (heating permitted) to obtain homogeneous solutions or sample dispersions. Parameters that can be set are time (s), temperature (℃) and angular velocity (rpm).
5. Centrifuge station: For separating mixtures of liquids and solid particles. Parameters that can be set are time (s) and angular velocity (rpm).
6. Calcination station: For calcining and heating samples. Parameters that can be set are time (s), temperature (℃) and heating rate (℃/min).
7. Aspiration station: For aspirating the waste liquid above the sample after centrifugation.
8. Drying station: For drying samples. Parameters that can be set are time (s) and temperature (℃).
9. Ultrasonic station: For crushing solid samples or accelerating sample dissolution. The parameter that can be set is the time (s).
10. Encapsulation station: For encapsulating reaction vessels under vacuum. 
11. Photocatalytic station: For carrying out light irradiation with simultaneous agitation. The parameter that can be set is the time (s).
12. Gas chromatography station: For measuring the gas production of reaction systems.
13. Sample preparation station: For preparing samples for characterization or measurement. Specific procedures depend on the type of sample. The parameter that can be set is the type of sample.
14. Raman spectroscopy station: For measuring Raman spectra of samples.
15. Infrared spectroscopy station: For measuring the FT-IR spectra of samples.
16. UV-vis spectroscopy station: For measuring the absorption of UV-vis light of samples.
17. Fluorescence spectroscopy station: For measuring the fluorescence spectrum of samples.
18. PXRD station: For determining the phase composition of samples.
19. LIBS station: For measuring the concentration of major and trace elements in solid, liquid, or air samples.
20. Electrocatalytic station: For performing electrocatalytic tests by a three-electrode system.'''
    return station_list

@tool
def query_robotAPI_list(str):
    """get the list of available high-level API functions for robots"""
    robotAPI_list=''' 1. locate(station_name: str) -> pose
#Get the manipulation pose of the station_name station. 
2. move(station_name: str) -> None
#Move to the station_name station.
3. take_bottle(rack_idx: int, bottle_idx: int, station_name: str) -> None
#Take the bottle defined by rack_idx and bottle_idx from the station_name station to the robot. 
4. put_bottle(rack_idx: int, bottle_idx: int, station_name: str) -> None
#Put the bottle defined by rack_idx and bottle_idx from the robot to the station_name station. 
5. take_rack(rack_idx: int, station_name: str) -> None
#Take the rack defined by rack_idx from the station_name station to the robot.
6. put_rack(rack_idx: int, station_name: str) -> None
#Put the rack defined by rack_idx from the robot to the station_name station.
7. command (station_name: str, instruction: str) -> None
#Send instruction to the station_name station, with the content defined by the instruction. 
The instructions for each station are as follows:
   7.1 Instruction for liquid station: 
      `instruction = {"type": "liquid_type", "mass": "paras"}`
      #The liquid station will add `type` liquid and `mass` grams into the bottle. Parameters that can be set are mass (g) and the type of liquid.
   7.2 Instruction for solid station: 
      `instruction = {"type": "solid_type", "mass": "paras"}`
      #The solid station will add `type` powder and `mass` grams into the bottle. Parameters that can be set are mass (g) and the type of solid.
   7.3 Instruction for magnetic stirring station:
      `instruction = {"rpm": "paras1", "temperature": "paras2", "time": "paras3"}`
      #The magnetic stirring station will set the speed defined by `rpm` and heat the rack to the temperature defined by `temperature` and stir for `time` seconds. Parameters that can be set are time (s), temperature (℃) and angular velocity (rpm).
   7.4 Instruction for centrifuge station: 
      `instruction = {"rpm": "paras1", "time": "paras2"}`
      #The centrifuge station will set the speed defined by `rpm` and centrifuge for `time` seconds. Parameters that can be set are time (s) and angular velocity (rpm).
   7.5 Instruction for calcination station: 
      `instruction = {"temperature": "paras1", "time": "paras2", "heating rate": "paras3"}`
      #The calcination station will set a heating speed defined by `heating rate`, heat up to the temperature defined by `temperature`, and then continue for `time` seconds. Parameters that can be set are time (s), temperature (℃) and heating rate (℃/min).
   7.6 Instruction for drying station: 
      `instruction = {"temperature": "paras1", "time": "paras2"}`
      #The drying station will heat the rack to the temperature defined by `temperature` and dry for `time` seconds. Parameters that can be set are time (s) and temperature (℃).
   7.7 Instruction for ultrasonic station: 
      `instruction = {"time": "paras"}`
      #The ultrasonic station will run for `time` seconds. The parameter that can be set is the time (s).
   7.8 Instruction for photocatalytic station: 
      `instruction = {"time": "paras"}`
      #The photocatalytic station will run for `time` seconds. The parameter that can be set is the time (s).
   7.9 Instruction for sample preparation station: 
      `instruction = {"sample": "sample_type"}`
      #The sample preparation station will make the sample defined by `sample`. The parameter that can be set is the type of sample.
   7.10 Instruction for other stations: 
      `instruction = {}`
      Do not need to send instructions to these stations. 
8. wait(station_name: str) -> None
#Wait until the station_name station's operation is completed.'''
    return robotAPI_list

@tool
def query_pretrained_model_library(str):
    """query pre-trained model library, `str` usually includes the name of the experiment that needs to be designed or the experiment object made or synthesize"""
    str = str.lower()
    # `ModelSearch` function requests access to the Model Library, with a matching model provided by the local Library. The Model Library is temporarily not open for external access. It need to be replaced with corresponding resources.
    index, PredictionFunction = ModelSearch(str)
    return index, PredictionFunction

@tool
def fuse_the_model(index,ExperimentalDataPath):
    """the model fusion tool, expand a pre-trained neural-network model by appending additional hidden layers to create a fused model, `index` is the index of the pre-trained model in the Model Library, `ExperimentalDataPath` is the experimental data"""
    # `ModelFuse` function requests access to the Model Library and and experimental data. These are temporarily not open for external access. It need to be replaced with corresponding resources.
    FusedModelProgram = ModelFuse(index，ExperimentalDataPath)
    return FusedModelProgram

@tool
def Bayesian_optimizer(FusedModelProgram,ExperimentalDataPath):
    """the Bayesian optimizer, perform random Bayesian optimization on the given model, and finally provide Bayesian optimization code. `FusedModelProgram` is the program for the given model, `ExperimentalDataPath` is the experimental data"""
    # `BayesianOptimizer` function is an LLM-based agent, pre-prompted to write Bayesian optimization code. Use it directly as a packaged tool here.
    BayesianProgram = BayesianOptimizer(FusedModelProgram,ExperimentalDataPath)
    return BayesianProgram

@tool
def LiteratureReader(PassingInfo):
    """Read literature to obtain the chemical knowledge required to be read, such as chemical elements or reactants. `PassingInfo` refers to the description of the chemical reaction or the material to be synthesized as provided."""
    # `LR` function is the Literature Reader Agent. Use it directly as a packaged tool here.
    Answer = LR(PassingInfo)
    return Answer

@tool
def ExperimentDesigner(PassingInfo):
    """Design an experimental procedure with chemical experimental parameters. `Passing Info` includes the name of the experiment to be designed or the target object for synthesis and the chemical experimental parameters."""
    # `ED` function is the Experiment Designer Agent. Use it directly as a packaged tool here.
    Answer = ED(PassingInfo)
    return Answer

@tool
def RobotOperator(PassingInfo):
    """Conduct robot experiments according to the experimental procedure. `Passing Info` contains the designed experimental procedure to be executed."""
    # `RO` function is the Robot Operator Agent. Use it directly as a packaged tool here.
    Answer = RO(PassingInfo)
    return Answer

@tool
def ComputationPerformer(PassingInfo):
    """Calculate or optimize tasks based on requirements. `Passing Info` includes the description of the computational task provided and Experimental data generated by the robotic experiment."""
    # `CP` function is the Computation Performer Agent. Use it directly as a packaged tool here.
    Answer = CP(PassingInfo)
    return Answer