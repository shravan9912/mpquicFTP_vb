import h5py
import sys

def print_attrs(name, obj):
    print(name)
    for key, val in obj.attrs.items():
        print("    %s: %s" % (key, val))
        for element in val:
           print(name+"/"+element)
           print("        %s" % (obj["/"+name+"/"+element].value))

f = h5py.File(sys.argv[1], 'r')
f.visititems(print_attrs)
