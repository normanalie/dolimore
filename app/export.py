import csv
import os

class Export:
    @classmethod
    def path(cls, lst: list()) -> str():
        """
        Join the lst into a single path and create it if necessary. 
        Return the path. 
        """
        path = os.path.join(*lst)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        dir = os.path.join(current_dir, os.path.dirname(path))
        if not os.path.exists(dir):
            os.makedirs(dir)
        return path

    @classmethod
    def csv(cls, lst: list(), path: str())->str():
        """
        Take the full path with filename and a list of values and write them in a single row in a csv file. 
        Return the path of the file or 1 if error.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, path)
        if path.endswith(".csv"):
            with open(path, "w") as f:
                writer = csv.writer(f)
                writer.writerow(lst)
            return path
        return 1

    
        
        
