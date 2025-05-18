from src.classes.Tutor import *


tuition_job_set:set = {CHEMISTRY,MATH}
tutor_set:set = {COMPUTING,MATH,CHEMISTRY,PHYSICS}
print(tuition_job_set.intersection(tutor_set))