import matplotlib.pyplot as plt
#main
def main():
    fig=plt.figure(figsize=(6.7,5))
    ax = plt.gca()
    ax.set_xlim(0,500000)
    with open('files/rsel.csv','r') as f1:
        list1=[]
        list2=[]
        f1.readline()
        for line in f1:
            line=line.split(',')
            line[-1]=line[-1][:-2]
            line = [float(i) for i in line]
            list1.append(line[1])
            list2.append((sum(line)-line[0]-line[1])/(len(line)-2))
        plt.plot(list1,list2,label="1-Evol-RS")
    with open('files/cel-rs.csv','r') as f1:
        list1=[]
        list2=[]
        f1.readline()
        for line in f1:
            line=line.split(',')
            line[-1]=line[-1][:-2]
            line = [float(i) for i in line]
            list1.append(line[1])
            list2.append((sum(line)-line[0]-line[1])/(len(line)-2))
        plt.plot(list1,list2,label="1-Coev-RS")
    with open('files/2cel-rs.csv','r') as f1:
        list1=[]
        list2=[]
        f1.readline()
        for line in f1:
            line=line.split(',')
            line[-1]=line[-1][:-2]
            line = [float(i) for i in line]
            list1.append(line[1])
            list2.append((sum(line)-line[0]-line[1])/(len(line)-2))
        plt.plot(list1,list2,label="2-Coev-RS")
    with open('files/cel.csv','r') as f1:
        list1=[]
        list2=[]
        f1.readline()
        for line in f1:
            line=line.split(',')
            line[-1]=line[-1][:-2]
            line = [float(i) for i in line]
            list1.append(line[1])
            list2.append((sum(line)-line[0]-line[1])/(len(line)-2))
        plt.plot(list1,list2,label="1-Coev",color="black")
    with open('files/2cel.csv','r') as f1:
        list1=[]
        list2=[]
        f1.readline()
        for line in f1:
            line=line.split(',')
            line[-1]=line[-1][:-2]
            line = [float(i) for i in line]
            list1.append(line[1])
            list2.append((sum(line)-line[0]-line[1])/(len(line)-2))
        plt.plot(list1,list2,label="2-Coev",color="magenta")
    plt.legend(loc="lower right")
    plt.savefig('myplot.pdf')
    plt.close()
if __name__ == '__main__':
    main()