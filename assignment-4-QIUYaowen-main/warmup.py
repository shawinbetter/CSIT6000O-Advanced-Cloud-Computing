# Databricks notebook source
# MAGIC %md
# MAGIC ![Spark Logo](http://spark-mooc.github.io/web-assets/images/ta_Spark-logo-small.png) + ![Python Logo](http://spark-mooc.github.io/web-assets/images/python-logo-master-v3-TM-flattened_small.png)
# MAGIC 
# MAGIC # **Warmup Notebook: Testing Databricks Environment**
# MAGIC 
# MAGIC *Note: This notebook is merely a warmup exercise and not subject to grading.*
# MAGIC 
# MAGIC This notebook will show you how to install the test libraries, test basic notebook functionality, and export a notebook for submitting. To move through the notebook, just run each of the cells. You will not need to solve any problems to complete this lab. You can run a cell by pressing "shift-enter", which will compute the current cell and advance to the next cell, or by clicking in a cell and pressing "control-enter", which will compute the current cell and remain in that cell.
# MAGIC 
# MAGIC **Within this notebook we will cover:**
# MAGIC 
# MAGIC - *Part 1*: Testing Spark Functionality
# MAGIC - *Part 2*: Checking Test Helper
# MAGIC - *Part 3*: Checking Matplotlib Support
# MAGIC - *Part 4*: Checking KaTeX Support
# MAGIC - *Part 5*: Exporting Notebook

# COMMAND ----------

# MAGIC %md
# MAGIC #### Prelude
# MAGIC 
# MAGIC **(1a) Importing Test Helper**
# MAGIC 
# MAGIC The class helper library "test_helper" is published in the [GitHub repository](https://github.com/hpec/test_helper) as [test_helper](https://pypi.org/project/test_helper/) package. Here we can manually import the "Test" class for use.

# COMMAND ----------

# initialize the Test class
import hashlib

class TestFailure(Exception):
    pass
class PrivateTestFailure(Exception):
    pass

class Test(object):
    passed = 0
    numTests = 0
    failFast = False
    private = False

    @classmethod
    def setFailFast(cls):
        cls.failFast = True

    @classmethod
    def setPrivateMode(cls):
        cls.private = True

    @classmethod
    def assertTrue(cls, result, msg=""):
        cls.numTests += 1
        if result == True:
            cls.passed += 1
            print("1 test passed.")
        else:
            print("1 test failed. " + msg)
            if cls.failFast:
                if cls.private:
                    raise PrivateTestFailure(msg)
                else:
                    raise TestFailure(msg)

    @classmethod
    def assertEquals(cls, var, val, msg=""):
        cls.assertTrue(var == val, msg)

    @classmethod
    def assertEqualsHashed(cls, var, hashed_val, msg=""):
        cls.assertEquals(cls._hash(var), hashed_val, msg)

    @classmethod
    def printStats(cls):
        print("{0} / {1} test(s) passed.".format(cls.passed, cls.numTests))

    @classmethod
    def _hash(cls, x):
        return hashlib.sha1(str(x).encode('utf-8')).hexdigest()

# COMMAND ----------

# MAGIC %md
# MAGIC **(1b) Uploading Text File**
# MAGIC 
# MAGIC Now we update to Databricks a text file which will be used in next part. 
# MAGIC 
# MAGIC - **Step 1**: Download [shakesper.txt](https://raw.githubusercontent.com/hkust-comp4651/assets/master/assignment-4/shakespere.txt) to your computer.
# MAGIC 
# MAGIC - **Step 2**: Go to the uploading page by selecting "Data" and then "Create Table".
# MAGIC 
# MAGIC <br/>
# MAGIC 
# MAGIC ![add_data](https://raw.githubusercontent.com/hkust-comp4651/assets/master/assignment-4/create_table_small.png)
# MAGIC 
# MAGIC <br/>
# MAGIC 
# MAGIC - **Step 3**: Click "browse" to select the file you have just downloaded.
# MAGIC 
# MAGIC <br/>
# MAGIC 
# MAGIC ![browse_file](https://raw.githubusercontent.com/hkust-comp4651/assets/master/assignment-4/browse_file_small.png)

# COMMAND ----------

# MAGIC %md
# MAGIC #### **Part 1: Testing Spark functionality**
# MAGIC 
# MAGIC **(1a) Common Operators**

# COMMAND ----------

# check whether Spark is working properly
largeRange = sc.parallelize(range(100000))
reduceTest = largeRange.reduce(lambda a, b: a + b)
filterReduceTest = largeRange.filter(lambda x: x % 7 == 0).sum()

print(reduceTest)
print(filterReduceTest)

# AssertionError will be raised if Spark is malfunctioning
assert reduceTest == 4999950000
assert filterReduceTest == 714264285

# COMMAND ----------

# MAGIC %md
# MAGIC **(1b) Loading Text File**

# COMMAND ----------

# load text file with sc.textFile
import os.path
filePath = 'dbfs:/FileStore/tables/shakespere.txt'

rawData = sc.textFile(filePath)
shakespeareCount = rawData.count()

print(shakespeareCount)

assert shakespeareCount == 149689

# COMMAND ----------

# MAGIC %md
# MAGIC #### ** Part 2: Checking Test Helper **
# MAGIC 
# MAGIC ** (2a) Hash Comparison **

# COMMAND ----------

# Check our testing library/package
# This should print '1 test passed.' on two lines
twelve = 12
Test.assertEquals(twelve, 12, 'twelve should equal 12')
Test.assertEqualsHashed(twelve, '7b52009b64fd0a2a49e6d8a939753077792b0554',
                        'twelve, once hashed, should equal the hashed value of 12')

# COMMAND ----------

# MAGIC %md
# MAGIC **(2b) List Comparison**

# COMMAND ----------

# This should print '1 test passed.'
unsortedList = [(5, 'b'), (5, 'a'), (4, 'c'), (3, 'a')]
Test.assertEquals(sorted(unsortedList), [(3, 'a'), (4, 'c'), (5, 'a'), (5, 'b')],
                  'unsortedList does not sort properly')

# COMMAND ----------

# MAGIC %md
# MAGIC #### ** Part 3: Checking Matplotlib Support **
# MAGIC 
# MAGIC ** (3a) Our first plot **
# MAGIC 
# MAGIC After executing the code cell below, you should see a plot with 50 blue circles.  The circles should start at the bottom left and end at the top right.

# COMMAND ----------

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from math import log

# function for generating plot layout
def preparePlot(xticks, yticks, figsize=(10.5, 6), hideLabels=False, gridColor='#999999', gridWidth=1.0):
    plt.close()
    fig, ax = plt.subplots(figsize=figsize, facecolor='white', edgecolor='white')
    ax.axes.tick_params(labelcolor='#999999', labelsize='10')
    for axis, ticks in [(ax.get_xaxis(), xticks), (ax.get_yaxis(), yticks)]:
        axis.set_ticks_position('none')
        axis.set_ticks(ticks)
        axis.label.set_color('#999999')
        if hideLabels: axis.set_ticklabels([])
    plt.grid(color=gridColor, linewidth=gridWidth, linestyle='-')
    map(lambda position: ax.spines[position].set_visible(False), ['bottom', 'top', 'left', 'right'])
    return fig, ax

# generate layout and plot data
x = range(1, 50)
y = [log(x1 ** 2) for x1 in x]
fig, ax = preparePlot(range(5, 60, 10), range(0, 12, 1))
plt.scatter(x, y, s=14**2, c='#d6ebf2', edgecolors='#8cbfd0', alpha=0.75)
ax.set_xlabel(r'$range(1, 50)$'), ax.set_ylabel(r'$\log_e(x^2)$')

# call display() to show the figure
display(fig)

# COMMAND ----------

# MAGIC %md
# MAGIC #### ** Part 4: Checking KaTeX Support **
# MAGIC 
# MAGIC Databricks notebooks render LaTeX formulae with [KaTeX](https://katex.org/). [Here](https://katex.org/docs/supported.html) is a list of all supported symbols and macros.
# MAGIC 
# MAGIC **Tip**: The common newline `\\` in LaTeX is not allowed here, so you have to use `\cr` instead.
# MAGIC 
# MAGIC ** (4a) Gradient descent formula **
# MAGIC 
# MAGIC You should see a formula on the line below this one: $$ \small \mathbf{w}_{i+1} = \mathbf{w}_i - \alpha_i \sum_j (\mathbf{w}_i^\top\mathbf{x}_j  - y_j) \mathbf{x}_j \,.$$
# MAGIC  
# MAGIC This formula is included inline with the text and is \\( \small (\mathbf{w}^\top \mathbf{x} - y) \mathbf{x} \\).
# MAGIC 
# MAGIC ** (4b) Log loss formula **
# MAGIC 
# MAGIC This formula shows log loss for single point. Log loss is defined as: 
# MAGIC $$ 
# MAGIC \small
# MAGIC loss(p, y) = \begin{cases}
# MAGIC    -\log(p)   & \text{if } y = 1 \cr
# MAGIC    -\log(1-p) & \text{if } y = 0
# MAGIC \end{cases} 
# MAGIC $$

# COMMAND ----------

# MAGIC %md
# MAGIC #### ** Part 5: Exporting Notebook**
# MAGIC 
# MAGIC The export and download the notebook from Databricks, click on "File", then select "Export" and "Source File". This will export your notebook as a .py file to your computer.
# MAGIC 
# MAGIC <br/>
# MAGIC 
# MAGIC ![export_notebook](https://raw.githubusercontent.com/hkust-comp4651/assets/master/assignment-4/export_notebook_small.png)
# MAGIC 
# MAGIC <br/>
# MAGIC 
# MAGIC When you've done coding, you can add the exported .py file to the git repo, commit and push it to GitHub for grading.
