from opentrons import protocol_api
import random

metadata = {"protocolName":"My Protocol",
   "author": "OT-Mation",
   "description": "debugging script for OT-Mation",
   "apiLevel": "2.10"}

def run(protocol: protocol_api.ProtocolContext):
   reagent_rack = protocol.load_labware("opentrons_24_aluminumblock_nest_1.5ml_snapcap", location=1)
   sample_rack = protocol.load_labware("corning_384_wellplate_112ul_flat", location=2)
   tiprack50ul = protocol.load_labware("opentrons_96_tiprack_300ul", location=4)
   tiprack10ul = protocol.load_labware("opentrons_96_tiprack_20ul", location=5)
   trash = protocol.load_labware("agilent_1_reservoir_290ml", location=10)
   def pip_use(x):
      nonlocal pipette
      q = pipette1
      r = pipette2
      if q.min_volume > r.min_volume:
         big = q
         small = r
      else:
         big = r
         small = q
      if x < big.min_volume:
         pipette = small
      else:
         pipette = big
   
   def diluent_find():
      for key in components:
         for k in components[key]:
            if components[key][k]["Diluent"].lower() == "y":
               return components[key][k]["Well Location"]
   def well_blacklist(x):
      temp_variable = x
      escape = 0
      nonlocal blacklist
      nonlocal dup_list
      try:
         for i in x:
            print(i)
      except(TypeError):
         while escape == 0:
            if sample_rack.wells(temp_variable) in blacklist or temp_variable in dup_list:
               temp_variable = temp_variable + 1
            else:
               escape = 1
               dup_list.append(temp_variable)
         return(temp_variable)
      else:
         for q, i in enumerate(x):
            escape = 0
            while escape == 0:
               if sample_rack.wells(temp_variable[q]) in blacklist or temp_variable[q] in dup_list:
                  temp_variable[q] = temp_variable[q] + 1
               else:
                  dup_list.append(temp_variable[q])
                  escape = 1
         return(temp_variable)
   blacklist = sample_rack.columns(0) + sample_rack.columns(-1) + sample_rack.rows(0) + sample_rack.rows(-1)
   dup_list = []
   replicates = 1
   def chunks(lst, n):
      temp = []
      for i in range(0,len(lst),n):
         temp.append(lst[i:i + n])
      return(temp)
   well_list = []
   well_counter = 0
   def randomiser(x):
      nonlocal well_list
      nonlocal well_counter
      nonlocal replicates
      if replicates == 1:
         pass
      else:
         well_counter = [int(x) for x in str(well_counter)]
         for q, i in enumerate(range(replicates)):
            if len(well_counter) < replicates:
               well_counter.append(q)
      for key in x:
         well_counter = well_blacklist(well_counter)
         if replicates == 1:
            well_list.append(well_counter)
         else:
            well_list.extend(well_counter)
      random.shuffle(well_list)
      key_list = []
      print_out = {}
      for key in x:
         key_list.append(key)
      if replicates > 1:
         well_list = chunks(well_list, replicates)
      for i, key in enumerate(key_list):
         print_out[key] = well_list[i]
      with open("Randomisation.txt", "+a") as file:
         file.write("Sample placement has been randomised as follows:\n\n" + "{}\n".format(print_out) + "\n" +
      "Sample number refers to the row within the Experimental Parameters.csv file. Location number is the well via zero indexing (0 = A1, 1 = B1 etc.)")
   
   replicates = 1
   pipette1 = protocol.load_instrument(instrument_name="p50_single",
       mount="right",
       tip_racks=[tiprack50ul])
   pipette2 = protocol.load_instrument(instrument_name="p10_single",
       mount="left",
       tip_racks=[tiprack10ul])
   pipette = pipette1
   pipette1.flow_rate.aspirate = 150
   pipette1.flow_rate.dispense = 150
   pipette2.flow_rate.aspirate = 150
   pipette2.flow_rate.dispense = 150
   components = {'Master_Mix': {'Sample 0': {'Well Location': 'reagent_rack.wells("A1")', 'Volume': 370, 'Concentration': 100, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 46.0, 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N', 'Target Concentration': 1.0}, 'Sample 1': {'Well Location': 'reagent_rack.wells("A1")', 'Volume': 370, 'Concentration': 100, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 46.0, 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N', 'Target Concentration': 1.0}, 'Sample 2': {'Well Location': 'reagent_rack.wells("A1")', 'Volume': 370, 'Concentration': 100, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 46.0, 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N', 'Target Concentration': 1.0}, 'Sample 3': {'Well Location': 'reagent_rack.wells("A1")', 'Target Concentration': 1.0, 'Volume': 370, 'Concentration': 100, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 46.0, 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}, 'Sample 4': {'Well Location': 'reagent_rack.wells("A1")', 'Target Concentration': 1.0, 'Volume': 370, 'Concentration': 100, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 46.0, 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}, 'Sample 5': {'Well Location': 'reagent_rack.wells("A1")', 'Target Concentration': 1.0, 'Volume': 370, 'Concentration': 100, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 46.0, 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}, 'Sample 6': {'Well Location': 'reagent_rack.wells("A1")', 'Target Concentration': 1.0, 'Volume': 370, 'Concentration': 100, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 46.0, 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}, 'Sample 7': {'Well Location': 'reagent_rack.wells("A1")', 'Target Concentration': 1.0, 'Volume': 370, 'Concentration': 100, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 46.0, 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}}, 'Reagent_1': {'Sample 0': {'Well Location': 'reagent_rack.wells("A2")', 'Volume': 50, 'Concentration': 10, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N', 'Target Concentration': 0.2}, 'Sample 1': {'Well Location': 'reagent_rack.wells("A2")', 'Volume': 50, 'Concentration': 10, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N', 'Target Concentration': 0.2}, 'Sample 2': {'Well Location': 'reagent_rack.wells("A2")', 'Volume': 50, 'Concentration': 10, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N', 'Target Concentration': 0.2}, 'Sample 3': {'Well Location': 'reagent_rack.wells("A2")', 'Target Concentration': 0.2, 'Volume': 50, 'Concentration': 10, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}, 'Sample 4': {'Well Location': 'reagent_rack.wells("A2")', 'Target Concentration': 0.0, 'Volume': 50, 'Concentration': 10, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}, 'Sample 5': {'Well Location': 'reagent_rack.wells("A2")', 'Target Concentration': 0.0, 'Volume': 50, 'Concentration': 10, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}, 'Sample 6': {'Well Location': 'reagent_rack.wells("A2")', 'Target Concentration': 0.0, 'Volume': 50, 'Concentration': 10, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}, 'Sample 7': {'Well Location': 'reagent_rack.wells("A2")', 'Target Concentration': 0.0, 'Volume': 50, 'Concentration': 10, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}}, 'Reagent_2': {'Sample 0': {'Well Location': 'reagent_rack.wells("A3")', 'Volume': 50, 'Concentration': 10, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N', 'Target Concentration': 0.0}, 'Sample 1': {'Well Location': 'reagent_rack.wells("A3")', 'Volume': 50, 'Concentration': 10, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N', 'Target Concentration': 0.0}, 'Sample 2': {'Well Location': 'reagent_rack.wells("A3")', 'Volume': 50, 'Concentration': 10, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N', 'Target Concentration': 0.0}, 'Sample 3': {'Well Location': 'reagent_rack.wells("A3")', 'Target Concentration': 0.0, 'Volume': 50, 'Concentration': 10, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}, 'Sample 4': {'Well Location': 'reagent_rack.wells("A3")', 'Target Concentration': 0.2, 'Volume': 50, 'Concentration': 10, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}, 'Sample 5': {'Well Location': 'reagent_rack.wells("A3")', 'Target Concentration': 0.2, 'Volume': 50, 'Concentration': 10, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}, 'Sample 6': {'Well Location': 'reagent_rack.wells("A3")', 'Target Concentration': 0.2, 'Volume': 50, 'Concentration': 10, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}, 'Sample 7': {'Well Location': 'reagent_rack.wells("A3")', 'Target Concentration': 0.2, 'Volume': 50, 'Concentration': 10, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}}, 'Reagent_3': {'Sample 0': {'Well Location': 'reagent_rack.wells("A4")', 'Volume': 20, 'Concentration': 10, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N', 'Target Concentration': 0.2}, 'Sample 1': {'Well Location': 'reagent_rack.wells("A4")', 'Volume': 20, 'Concentration': 10, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N', 'Target Concentration': 0.2}, 'Sample 2': {'Well Location': 'reagent_rack.wells("A4")', 'Volume': 20, 'Concentration': 10, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N', 'Target Concentration': 0.0}, 'Sample 3': {'Well Location': 'reagent_rack.wells("A4")', 'Target Concentration': 0.0, 'Volume': 20, 'Concentration': 10, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}, 'Sample 4': {'Well Location': 'reagent_rack.wells("A4")', 'Target Concentration': 0.2, 'Volume': 20, 'Concentration': 10, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}, 'Sample 5': {'Well Location': 'reagent_rack.wells("A4")', 'Target Concentration': 0.2, 'Volume': 20, 'Concentration': 10, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}, 'Sample 6': {'Well Location': 'reagent_rack.wells("A4")', 'Target Concentration': 0.0, 'Volume': 20, 'Concentration': 10, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}, 'Sample 7': {'Well Location': 'reagent_rack.wells("A4")', 'Target Concentration': 0.0, 'Volume': 20, 'Concentration': 10, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}}, 'Reagent_4': {'Sample 0': {'Well Location': 'reagent_rack.wells("A5")', 'Volume': 300, 'Concentration': 10, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N', 'Target Concentration': 0.0}, 'Sample 1': {'Well Location': 'reagent_rack.wells("A5")', 'Volume': 300, 'Concentration': 10, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N', 'Target Concentration': 0.0}, 'Sample 2': {'Well Location': 'reagent_rack.wells("A5")', 'Volume': 300, 'Concentration': 10, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N', 'Target Concentration': 0.2}, 'Sample 3': {'Well Location': 'reagent_rack.wells("A5")', 'Target Concentration': 0.2, 'Volume': 300, 'Concentration': 10, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}, 'Sample 4': {'Well Location': 'reagent_rack.wells("A5")', 'Target Concentration': 0.0, 'Volume': 300, 'Concentration': 10, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}, 'Sample 5': {'Well Location': 'reagent_rack.wells("A5")', 'Target Concentration': 0.0, 'Volume': 300, 'Concentration': 10, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}, 'Sample 6': {'Well Location': 'reagent_rack.wells("A5")', 'Target Concentration': 0.2, 'Volume': 300, 'Concentration': 10, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}, 'Sample 7': {'Well Location': 'reagent_rack.wells("A5")', 'Target Concentration': 0.2, 'Volume': 300, 'Concentration': 10, 'Target Volume': 50, 'Speed': 150, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}}, 'Reagent_5': {'Sample 0': {'Well Location': 'sample_rack.wells("A1")', 'Volume': 20, 'Concentration': 10, 'Target Volume': 50, 'Speed': 50, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N', 'Target Concentration': 0.4}, 'Sample 1': {'Well Location': 'sample_rack.wells("A1")', 'Volume': 20, 'Concentration': 10, 'Target Volume': 50, 'Speed': 50, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N', 'Target Concentration': 0.4}, 'Sample 2': {'Well Location': 'sample_rack.wells("A1")', 'Volume': 20, 'Concentration': 10, 'Target Volume': 50, 'Speed': 50, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N', 'Target Concentration': 0.4}, 'Sample 3': {'Well Location': 'sample_rack.wells("A1")', 'Target Concentration': 0.4, 'Volume': 20, 'Concentration': 10, 'Target Volume': 50, 'Speed': 50, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}, 'Sample 4': {'Well Location': 'sample_rack.wells("A1")', 'Target Concentration': 0.2, 'Volume': 20, 'Concentration': 10, 'Target Volume': 50, 'Speed': 50, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}, 'Sample 5': {'Well Location': 'sample_rack.wells("A1")', 'Target Concentration': 0.2, 'Volume': 20, 'Concentration': 10, 'Target Volume': 50, 'Speed': 50, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}, 'Sample 6': {'Well Location': 'sample_rack.wells("A1")', 'Target Concentration': 0.2, 'Volume': 20, 'Concentration': 10, 'Target Volume': 50, 'Speed': 50, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}, 'Sample 7': {'Well Location': 'sample_rack.wells("A1")', 'Target Concentration': 0.2, 'Volume': 20, 'Concentration': 10, 'Target Volume': 50, 'Speed': 50, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}}, 'Reagent_6': {'Sample 0': {'Well Location': 'sample_rack.wells("A2")', 'Volume': 15, 'Concentration': 10, 'Target Volume': 50, 'Speed': 50, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N', 'Target Concentration': 0.0}, 'Sample 1': {'Well Location': 'sample_rack.wells("A2")', 'Volume': 15, 'Concentration': 10, 'Target Volume': 50, 'Speed': 50, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N', 'Target Concentration': 0.0}, 'Sample 2': {'Well Location': 'sample_rack.wells("A2")', 'Volume': 15, 'Concentration': 10, 'Target Volume': 50, 'Speed': 50, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N', 'Target Concentration': 0.0}, 'Sample 3': {'Well Location': 'sample_rack.wells("A2")', 'Target Concentration': 0.0, 'Volume': 15, 'Concentration': 10, 'Target Volume': 50, 'Speed': 50, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}, 'Sample 4': {'Well Location': 'sample_rack.wells("A2")', 'Target Concentration': 0.2, 'Volume': 15, 'Concentration': 10, 'Target Volume': 50, 'Speed': 50, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}, 'Sample 5': {'Well Location': 'sample_rack.wells("A2")', 'Target Concentration': 0.2, 'Volume': 15, 'Concentration': 10, 'Target Volume': 50, 'Speed': 50, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}, 'Sample 6': {'Well Location': 'sample_rack.wells("A2")', 'Target Concentration': 0.2, 'Volume': 15, 'Concentration': 10, 'Target Volume': 50, 'Speed': 50, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}, 'Sample 7': {'Well Location': 'sample_rack.wells("A2")', 'Target Concentration': 0.2, 'Volume': 15, 'Concentration': 10, 'Target Volume': 50, 'Speed': 50, 'Transfer Volume': 'True', 'Percent': 'N', 'Mass per ul': 'N', 'Diluent': 'N', 'Delute': 'N'}}}
   
   containers = {'reagent_rack': {'Labware': 'opentrons_24_aluminumblock_nest_1.5ml_snapcap', 'Slot': 1, 'Working Volume': 1000, 'Source': 'Y', 'Mixing': 'N', 'Final': 'N'}, 'sample_rack': {'Labware': 'corning_384_wellplate_112ul_flat', 'Slot': 2, 'Working Volume': 50, 'Source': 'N', 'Mixing': 'N', 'Final': 'Y'}, 'tiprack50ul': {'Labware': 'opentrons_96_tiprack_300ul', 'Slot': 4, 'Working Volume': 0, 'Source': 'N', 'Mixing': 'N', 'Final': 'N'}, 'tiprack10ul': {'Labware': 'opentrons_96_tiprack_20ul', 'Slot': 5, 'Working Volume': 0, 'Source': 'N', 'Mixing': 'N', 'Final': 'N'}, 'trash': {'Labware': 'agilent_1_reservoir_290ml', 'Slot': 10, 'Working Volume': 0, 'Source': 'N', 'Mixing': 'N', 'Final': 'N'}}
   
   No_sample = {}
   well_assign = 0
   for key in components:
      for k in components[key]:
         if k in No_sample.keys():
            pass
         else:
            No_sample[k] = {}
            No_sample[k]["Location"] = well_assign
            No_sample[k]["Volume"] = 0
            well_assign = well_assign + 1
   for key in components:
      for k in components[key]:
         if components[key][k]["Diluent"].lower() == "y":
            pass
         else:
            if components[key][k]["Transfer Volume"] == "True":
               if components[key][k]["Percent"].lower() == "y":
                  if components[key][k]["Target Concentration"] < 1:
                     components[key][k]["Transfer Volume"] = (components[key][k]["Target Volume"]*components[key][k]["Target Concentration"])
                  else:
                     components[key][k]["Transfer Volume"] = (components[key][k]["Target Volume"]*((components[key][k]["Target Concentration"])/100))
               else:
                  if components[key][k]["Mass per ul"].lower() == "y":
                     components[key][k]["Transfer Volume"] = (components[key][k]["Target Concentration"]/components[key][k]["Concentration"])
                  else:
                     components[key][k]["Transfer Volume"] = (components[key][k]["Target Concentration"]*components[key][k]["Target Volume"])/components[key][k]["Concentration"]
            if k in No_sample.keys():
                  No_sample[k]["Volume"] = No_sample[k]["Volume"] + components[key][k]["Transfer Volume"]
   
   eval_dict = {}
   eval_dict["reagent_rack"] = reagent_rack
   eval_dict["sample_rack"] = sample_rack
   eval_dict["tiprack50ul"] = tiprack50ul
   eval_dict["tiprack10ul"] = tiprack10ul
   eval_dict["trash"] = trash
   for key in components:
      for k in components[key]:
         if components[key][k]["Transfer Volume"] == 0:
            pass
         else:
            if components[key][k]["Diluent"].lower() == "y":
               pass
            else:
               pip_use(components[key][k]["Transfer Volume"])
               pipette.flow_rate.aspirate = components[key][k]["Speed"] 
               pipette.flow_rate.dispense = components[key][k]["Speed"] 
               if components[key][k]["Transfer Volume"] <(pipette.max_volume/2):
                  pipette.transfer(components[key][k]["Transfer Volume"], eval(components[key][k]["Well Location"], eval_dict), sample_rack.wells(No_sample[k]["Location"]), new_tip="always", blow_out=False)
               else:
                  pipette.transfer(components[key][k]["Transfer Volume"], eval(components[key][k]["Well Location"], eval_dict), sample_rack.wells(No_sample[k]["Location"]), new_tip="always", blow_out="True")
   for key in No_sample:
      top_up = 50 - No_sample[key]["Volume"]
      if top_up < 1:
         pass
      else:
         pip_use(top_up)
         pipette.transfer(top_up, eval(diluent_find(), eval_dict), sample_rack.wells(No_sample[key]["Location"]), new_tip = "always", mix_after=[5,(pipette.max_volume/2)])