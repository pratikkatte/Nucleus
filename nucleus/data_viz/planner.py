import os
from pydantic import BaseModel, Field
from typing import List
from .dependencies import BAM_VISUALIZATION

def plan(input_filepath, session, message_printer):
    filename, file_ext = os.path.splitext(input_filepath)
    if file_ext == '.bam':
        if os.path.exists(input_filepath):
            file_requirements = bamFileReq(input_filepath, file_ext, session, message_printer)
            config = generate_config(file_ext, file_requirements)
            return config
        return None

def generate_config(ext, file_requirements):
    """
    """
    if ext=='.bam':
        assembly = {
                "name": 'NC_045512',

                "sequence": {
                    "type": 'ReferenceSequenceTrack',
                    "trackId": 'GRCh38-ReferenceSequenceTrack',
                    "adapter": {
                        "type": 'IndexedFastaAdapter',
                        "fastaLocation": {
                            "uri": f'http://127.0.0.1:8000/uploads/{file_requirements[".fa"]}',
                            },
                        "faiLocation": {
                            "uri": f'http://127.0.0.1:8000/uploads/{file_requirements[".fai"]}',
                            },
                        },
                    },
                }
        track = [{
        "type": 'AlignmentsTrack',
        "trackId": "genes", 
        "name": 'spike-in_bams_file_0.bam',
        "assemblyNames": ['NC_045512'],
        "category": ['Genes'],
        "adapter": {
          "type": 'BamAdapter',
          "bamLocation": {
            "uri": f'http://127.0.0.1:5000/uploads/{file_requirements[".bam"]}',
          },
          "index": {
            "location": {
              "uri": f'http://127.0.0.1:5000/uploads/{file_requirements[".bai"]}',
            },
          },
        }
    }]
    
    return {
        "assembly": assembly, 
        "track": track
        }



def bamFileReq(bamfile, ext, session, message_printer):
    """
    """
    requirements = BAM_VISUALIZATION

    prefix_text = f"In order display {bamfile}. \nFollowing input file types are required: \n "
    prefix_text += "\n".join([f"{i}. {key} file" for i, (key, value) in enumerate(requirements.items()) if key != ext])

    message_printer.assistant_message(prefix_text)



    all_file_quries = []

    
    for i, (key, value) in enumerate(requirements.items()):
        if key == ext:
            input_file_path = bamfile
        else:
            input_file_path = ""
        
        file_query = FileQuery(
            id=i,
            file_path=input_file_path,  # Replace with an actual file path
            file_type=key
        )
        all_file_quries.append(file_query)

    visualization_planner = VisualizationPlanner(file_queries=all_file_quries)
    
    all_files_required = visualization_planner.execute(session, message_printer)
    return all_files_required

class FileQuery(BaseModel):
    """
    """

    id: int = Field(..., description="Unique id of the query")
    file_path: str = Field(default=None, description="file required to display")
    file_type: str = Field(..., description="file extenstion")

    dependancies: int = Field(
        default=0,
        description="not needed now but maybe in future")
    
    def check_file(self, input_file):
        if input_file:
            filename, file_ext = os.path.splitext(input_file)
            if os.path.exists(input_file) and file_ext == self.file_type:
                return True
        return False

    def execute(self, required_files, session, message_printer):
        """
        """ 
        if self.check_file(self.file_path):
            required_files[self.file_type] = self.file_path
            return required_files
        else:
            while True:
                user_input = session.prompt(f"\n Please provide the {self.file_type} file : ")
                
                if self.check_file(user_input):
                    required_files[self.file_type] = user_input
                    return required_files
                else:
                    message_printer.assistant_message("Please provide the correct file.")

class VisualizationPlanner(BaseModel):
    """
    """
    file_queries: List[FileQuery] = Field(
        ..., description="list of files required to get from user"
    )
    required_files: dict = Field(default={}, description="required files")

    def dependencies(self, id: List[int]) -> List[FileQuery]:
        """
        not needed for now. but might be neded in future. 
        """
        pass

    def execute(self, session, message_printer):
        """
        """
        for query in self.file_queries:
            res = query.execute(
                self.required_files, session, message_printer
            )
            self.required_files = res
        return self.required_files
    
    
                