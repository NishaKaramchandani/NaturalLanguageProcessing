public class Stack
{
    static final int MAX = 1000;
    int top;
    String a[] = new String[MAX]; // Maximum size of Stack

    boolean isEmpty()
    {
        return (top < 0);
    }
    Stack()
    {
        top = -1;
    }

    boolean push(String x)
    {
        if (top >= MAX)
        {
            System.out.println("Stack Overflow");
            return false;
        }
        else
        {
            a[++top] = x;
            return true;
        }
    }

    String pop()
    {
        if (top < 0)
        {
            System.out.println("Stack Underflow");
            return "";
        }
        else
        {
            String x = a[top--];
            return x;
        }
    }
}
