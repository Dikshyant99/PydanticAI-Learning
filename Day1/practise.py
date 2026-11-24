
'''
name="Dikshyant"
age=21
height=5.8
is_student=None



age= age +1
print("New age is", age)

print("ha"*3)
print(int("42"))
print(int("42"+"2"))


print(f"{name}is{age} years ols and {height}feet tall")
'''
'''
word="Python"
print(word[0],word[-1],len(word))

title="Maths"
print(title.lower(),title.upper())


subjects="Maths,Physics,Engilsh".split(",")
print(subjects)
print("|".join(subjects))
'''
'''
#List
subjects=["Maths","Physics","English"]
subjects[0]= "Biology"
print(subjects)
subjects.append("Nepali")
print(subjects)
subjects.insert(1,"chemistry")
print(subjects)

subjects.pop()
print(subjects)
subjects.remove("English")
print(subjects)

#Sort vs sorted
marks=[40,20,80]
print(sorted(marks),marks)
marks.sort(reverse=True)
print(marks)
print(sum(marks),max(marks),min(marks))

#Alaising trap[]
a=[1,2,3]
b=a
b.append(4)
print(a)
c=a.copy()
c.append(5)
print(a,c)


#Tuples and unpacking
kathmandu=(27.7,80.1)
lat , lon =kathmandu
print(f"lat{lat},lon{lon}")

# tuples are immutable
#A list of tuples

assiggment=[("english","Nepali"),("Physics","Chemistry")]
print(assiggment)
print(assiggment[1][0])
'''

# Dictionary
assignment={
    "title":"essay","Subject":"English","done":False
}
assignment["title"]
print(assignment)
print(assignment["Subject"])  









