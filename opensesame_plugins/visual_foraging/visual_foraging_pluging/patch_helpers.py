from .serialization_helpers import deserialize_elements
from random import randint


def get_element_instances(elements, positions=None):
        element_types = elements
        element_instances = []
        for et in element_types:
            for i in range(0, int(et['amount'])):
                instance = {}
                for k in et.keys():
                    if k != 'amount':
                        instance[k] = et[k]
 
                instance['x'] = randint(0, 800)
                instance['y'] = randint(0, 800)
                element_instances.append(instance)
        
        return(element_instances)

