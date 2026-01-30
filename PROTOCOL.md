# Protocol for connecting to Cobot backend with this library
This protocol is used to establish connection over TCP. everything is sent in ASCII.

## Basic Commands

### ping
send: p
response: p
example:
```
<< 'p'
>> 'p'
```

### change velocity
send: v<decimal velocity>
response: no response
example:
```
<< 'v1.25'
```

### jog joints
send: j<+/-><joint no.>
response: no response
example:
```
<< 'j+0'
```

### cartesian jog
directions can be x(0),y(1),z(2),rx(3),ry(4),rz(5)
send: c<+/-><dirn>
response: no response
example:
```
<< 'c-3'
```

### stop all jogging
send: f
response: no response
```
<< 'f'
```

### open gripper
send: go
response: no response
send ping to see when operation completes
```
<< 'go'
// server might take time to complete this
// send ping to see when server is free
<< 'p'
>> 'p'
```

### close gripper
send: gc
response: no response
send ping to see when operation completes
```
<< 'gc'
<< 'p'
>> 'p'
```

### recovery by moveing to base
send: b
response: no response
send ping to confirm when operation ends
```
<< 'b'
<< 'p'
>> 'p'
```

### stop server
send: e
response: no response
```
<< 'e'
```

## Query Operations

### Joints
send: qj<v/p/t/a if j>
response: 6 decimal values with 3 decimal digits in a python list with no spaces, directly evaluatable using eval() in python
```
<< 'qjv'
>> '[0.234,1.200,0.000,0.000,1.023,0.500]'
```

### Cartesian Position
send: qp
response: 6 decimal values with 3 decimal digits in a python list with no spaces, directly evaluatable using eval() in python
```
<< 'qp'
>> '[1.234,0.340,0.203,0.040,0.047,0.076]'
```
