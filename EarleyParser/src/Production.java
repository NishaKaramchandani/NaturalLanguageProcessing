/**
 * This implements a production in a pcfg grammar
 *
 * @author Paul Chase: chaspau@iit.edu
 * @version 1.0
 */

import java.io.*;
import java.text.*;
import java.util.*;
import java.util.regex.*;

public class Production {
    float probability;
    String left;
    String right[];
    int dot;
    int start;
    int tree_number;

    //Production does double duty as a parse tree; this is for that.
    //therefore, has same number of children as right[], one for
    //each; if there is no child there, null is stored instead.
    List<Production> children;
    //parent is for the linking as well.
    Production parent;

    /**
     * Simple constructor, assumes no children, initializes everybody.
     */
    Production() {
        probability = 0.0f;
        left = "";
        right = null;
        dot = 0;
        start = 0;
        children = null;
        parent = null;
        tree_number = 0;
    }

    /**
     * Constructs a production with n right productions.
     */
    Production(int n) {
        this();
        right = new String[n];
        children = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            right[i] = null;
            children = null;
        }
    }

    /**
     * Constructs a production with the given right hand side.
     */
    Production(String[] rhs) {
        this(rhs.length);
        right = rhs;
    }

    /**
     * Copy constructor.
     */
    Production(Production p) {
        probability = p.probability;
        left = p.left;
        right = p.right;
        dot = p.dot;
        start = p.start;
        children = p.children;
        tree_number = p.tree_number;
    }

    /**
     * This creates a child of the production given its index.
     * This adds the child to the production and sets the parent for
     * the newly created child production.
     *
     * @param n the index on the right hand side where the child attaches
     * @return The newly created child
     */
    public final Production spawn(int n) {
        Production p = new Production();
        p.parent = this;
        children.add(p);
        return p;
    }

    /**
     * This creates a child of the production given its index.
     * This adds the child to the production and sets the parent for
     * the newly created child production.  The new child production
     * will be a copy of the production input as a parameter.
     *
     * @param n    the index on the right hand side where the child attaches
     * @param prod the production to copy the child from
     * @return The newly created child
     */
    public final Production spawn(int n, Production prod) {
        Production p = new Production(prod);
        p.parent = this;
        children.add(p);
        return p;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Production that = (Production) o;
        return Float.compare(that.probability, probability) == 0 &&
                dot == that.dot &&
                start == that.start &&
                tree_number == that.tree_number &&
                Objects.equals(left, that.left) &&
                Arrays.equals(right, that.right) &&
                Objects.equals(children, that.children) &&
                Objects.equals(parent, that.parent);
    }

    @Override
    public int hashCode() {

        int result = Objects.hash(probability, left, dot, start, tree_number, children, parent);
        result = 31 * result + Arrays.hashCode(right);
        return result;
    }

    /**
     * This returns true if the given production matches this one.
     * <p>
     * The comparison checks for identical productions only, down to the
     * placement of the dot.
     *
     * @param p The production to compare to.
     */
    public final boolean equals(Production p) {
        if (left != p.left || right.length != p.right.length || dot != p.dot || start != p.start || tree_number != p.tree_number)
            return false;
        for (int i = 0; i < right.length; i++)
            if (right[i] != p.right[i])
                return false;
        return true;
    }

    /**
     * Easy print.
     */
    public void print() {
        System.out.println(this.toString());
    }

    /**
     * Standard toString human-readable output.
     * Format:
     * startpos  left-- right1 . right2
     * with the dot moving about accordingly.
     */
    public String toString() {
        String ret = tree_number + "\t" + start + "\t" + left + "->";
        for (int i = 0; i < right.length; i++) {
            if (i == dot)
                ret = ret + "\t.";
            ret = ret + "\t" + right[i];
        }
        if (dot == right.length)
            ret = ret + "\t.";
        return ret;
    }

    /**
     * This prints a parse, a chain of productions.
     * TODO: Write this function!
     */
    public void recursivePrint() {

    }
}
