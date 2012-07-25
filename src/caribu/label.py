"""
Labels for the canestra file management.
"""

class Label(object):
    """ Label is an object to deals with can file cryptic label.
    It provide a way to store various information in one field.
    """
    def __init__(self,label='000000000000'):
        self._label=list(label)

    def _set_optical_id(self, optic_id):
        oid = list(str(optic_id))
        self._label[:-11] = oid
    def _get_optical_id(self):
        return int(''.join(self._label[:-11]))
    optical_id = property(_get_optical_id, _set_optical_id)

    def _get_plant_id(self):
        return int(''.join(self._label[-11:-6]))
    def _set_plant_id(self, plant_id):
        pid = list(str(plant_id))
        n = len(pid)
        if n < 5:
            p=list('0'*(5-n))
            pid = p+pid
        elif n > 5:
            raise 'Unable to add a too large plant id %d'%plant_id
        self._label[-11:-6] = pid

    plant_id = property(_get_plant_id, _set_plant_id)
    
    def _get_leaf_id(self):
        return int(''.join(self._label[-6:-3]))
    def _set_leaf_id(self, leaf_id):
        lid = list(str(leaf_id))
        n = len(lid)
        if n < 3:
            l=list('0'*(3-n))
            lid = l+lid
        elif n > 3:
            raise 'Unable to add a too large leaf id %d'%leaf_id
        self._label[-6:-3] = lid

    leaf_id = property(_get_leaf_id, _set_leaf_id)

    def _get_transparency(self):
        return int(bool(self.leaf_id))

    transparency = property(_get_transparency)

    def is_soil(self):
        return (self.optical_id == 0) and (self.transparency == 0)

    def is_leaf(self):
        return self.transparency > 0

    def is_stem(self):
        return (self.optical_id != 0) and (self.transparency == 0)

    def __str__(self):
        return ''.join(self._label)

    def _get_elt_id(self):
        return int(''.join(self._label[-3:]))

    def _set_elt_id(self, id):
        eid = list(str(id))
        n = len(eid)
        if n < 3:
            p=list('0'*(3-n))
            eid = p+eid
        elif n > 3:
            raise 'Unable to add a too large element id %d'%id
        self._label[-3:] = eid

    elt_id = property(_get_elt_id, _set_elt_id)

    
def _complete(l,length):
        if len(l) < length:
            l = l * (length / len(l)) + [l[i] for i in range(length % len(l))]
        return l
        
def _newlabel(opt,opak,plant,elt):
    lab = Label()
    lab.plant_id = plant
    lab.optical_id = opt
    lab.leaf_id = opak
    lab.elt_id = elt
    return lab
    
def encode_label(opt_id=1, opak=0, plant_id=1, elt_id=1, minlength = 1):
    """Create canlabels from list of properties to be encoded.
    canlabels allow to associate optical properties and geometry for Caribu
    properties are re-cycled to match the length of the longuest one
    minlength is the minimal length of the output
    
    """
    
    if not isinstance(opt_id, list):
        opt_id = [opt_id]
       
    if not isinstance(opak, list):
        opak = [opak]
        
    if not isinstance(plant_id, list):
        plant_id = [plant_id]
        
    if not isinstance(elt_id,list):
        elt_id = [elt_id]
        
    maxlen = max([max(map(len,[opt_id,opak,plant_id,elt_id])), minlength])
    
    opt_id, opak, plant_id, elt_id = map(lambda(x): _complete(x,maxlen),[opt_id,opak,plant_id,elt_id]) 
    
    return [str(_newlabel(opt_id[i],opak[i], plant_id[i], elt_id[i])) for i in range(maxlen)]
    
    
def decode_label(label):
    """ decode a (list of) canlabels into properties """
    
    if not isinstance(label, list):
        label = [label]
        
    properties = [(lab.optical_id, lab.transparency, lab.plant_id, lab.elt_id) for lab in (Label(labstring) for labstring in label)]    
    
    return zip(*properties)
    