# Databricks notebook source
# MAGIC %md
# MAGIC #![Spark Logo](http://spark-mooc.github.io/web-assets/images/ta_Spark-logo-small.png) + ![Python Logo](http://spark-mooc.github.io/web-assets/images/python-logo-master-v3-TM-flattened_small.png)
# MAGIC 
# MAGIC # **Word Count Lab: Building a Word Count Application**
# MAGIC 
# MAGIC This lab will build on the techniques covered in the Spark tutorial to develop a simple word count application.  The volume of unstructured text in existence is growing dramatically, and Spark is an excellent tool for analyzing this type of data.  In this lab, we will write code that calculates the most common words in the [Complete Works of William Shakespeare](http://www.gutenberg.org/ebooks/100) retrieved from [Project Gutenberg](https://www.gutenberg.org/).  This could also be scaled to find the most common words on the Internet.
# MAGIC 
# MAGIC ** During this lab we will cover: **
# MAGIC - *Part 1*: Creating RDDs
# MAGIC - *Part 2*: Counting with Pair RDDs
# MAGIC - *Part 3*: More Transformations
# MAGIC - *Part 4*: Applying to a File
# MAGIC 
# MAGIC > Note that, for reference, you can look up the details of the relevant methods in [Spark's Python API](https://spark.apache.org/docs/latest/api/python/reference/index.html)

# COMMAND ----------

# MAGIC %md
# MAGIC #### ** Part 1: Creating RDDs **
# MAGIC 
# MAGIC In this part of the lab, we will explore creating a base RDD with `parallelize` and using pair RDDs to count words.
# MAGIC 
# MAGIC ** (1a) Create a base RDD **
# MAGIC 
# MAGIC We'll start by generating a base RDD by using a Python list and the `sc.parallelize` method.  Then we'll print out the type of the base RDD.

# COMMAND ----------

wordsList = ['cat', 'elephant', 'rat', 'rat', 'cat']
wordsRDD = sc.parallelize(wordsList, numSlices=4)
# Print out the type of wordsRDD
print(type(wordsRDD))

# COMMAND ----------

# MAGIC %md
# MAGIC ** (1b) Capitalize and test **
# MAGIC 
# MAGIC Let's use a `map()` transformation to add the letter 's' to each string in the base RDD we just created. We'll define a Python function that returns the word with an 's' at the end of the word.  Please replace `<FILL IN>` with your solution.  If you have trouble, the next cell has the solution.  After you have defined `capitalize` you can run the third cell which contains a test.  If you implementation is correct it will print `1 test passed`.
# MAGIC 
# MAGIC This is the general form that exercises will take, except that no example solution will be provided.  Exercises will include an explanation of what is expected, followed by code cells where one cell will have one or more `<FILL IN>` sections.  The cell that needs to be modified will have `# TODO: Replace <FILL IN> with appropriate code` on its first line.  Once the `<FILL IN>` sections are updated and the code is run, the test cell can then be run to verify the correctness of your solution.  The last code cell before the next markdown section will contain the tests.

# COMMAND ----------

# TODO: Replace <FILL IN> with appropriate code
def capitalize(word):
    """Capitalize input word

    Args:
        word (str): A string.

    Returns:
        str: A string with all letters capitalized
    """
    return word.upper()

print(capitalize('cat'))

# COMMAND ----------

# One way of completing the function
def capitalize(word):
    return word.upper()

print(capitalize('cat'))

# COMMAND ----------

# Load in the testing code and check to see if your answer is correct
# If incorrect it will report back '1 test failed' for each failed test
# Make sure to rerun any cell you change before trying the test again
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

# TEST Pluralize and test (1b)
Test.assertEquals(capitalize('rat'), 'RAT', 'incorrect result: capitalize does not work properly')

# COMMAND ----------

# MAGIC %md
# MAGIC ** (1c) Apply `capitalize` to the base RDD **
# MAGIC 
# MAGIC Now pass each item in the base RDD into a [map()](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.RDD.map.html) transformation that applies the `capitalize()` function to each element. And then call the [collect()](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.RDD.collect.html) action to see the transformed RDD.

# COMMAND ----------

# TODO: Replace <FILL IN> with appropriate code
capitalRDD = wordsRDD.map(capitalize)
print(capitalRDD.collect())

# COMMAND ----------

# TEST Apply capitalize to the base RDD(1c)
Test.assertEquals(capitalRDD.collect(), ['CAT', 'ELEPHANT', 'RAT', 'RAT', 'CAT'],
                  'incorrect values for capitalRDD')

# COMMAND ----------

# MAGIC %md
# MAGIC ** (1d) Pass a `lambda` function to `map` **
# MAGIC 
# MAGIC Let's create the same RDD using a `lambda` function.

# COMMAND ----------

# TODO: Replace <FILL IN> with appropriate code
capitalLambdaRDD = wordsRDD.map(lambda x : x.upper())
print(capitalLambdaRDD.collect())

# COMMAND ----------

# TEST Pass a lambda function to map (1d)
Test.assertEquals(capitalLambdaRDD.collect(), ['CAT', 'ELEPHANT', 'RAT', 'RAT', 'CAT'],
                  'incorrect values for capitalLambdaRDD (1d)')

# COMMAND ----------

# MAGIC %md
# MAGIC ** (1e) Length of each word **
# MAGIC 
# MAGIC Now use `map()` and a `lambda` function to return the number of characters in each word.  We'll `collect` this result directly into a variable.

# COMMAND ----------

# TODO: Replace <FILL IN> with appropriate code
capitalLengths = (capitalRDD
                  .map(lambda x:len(x))\
                  .collect())
print(capitalLengths)

# COMMAND ----------

# TEST Length of each word (1e)
Test.assertEquals(capitalLengths, [3, 8, 3, 3, 3],
                  'incorrect values for pluralLengths')

# COMMAND ----------

# MAGIC %md
# MAGIC ** (1f) Pair RDDs **
# MAGIC 
# MAGIC The next step in writing our word counting program is to create a new type of RDD, called a pair RDD. A pair RDD is an RDD where each element is a pair tuple `(k, v)` where `k` is the key and `v` is the value. In this example, we will create a pair consisting of `('<word>', 1)` for each word element in the RDD.
# MAGIC 
# MAGIC We can create the pair RDD using the `map()` transformation with a `lambda()` function to create a new RDD.

# COMMAND ----------

# TODO: Replace <FILL IN> with appropriate code
wordPairs = wordsRDD.map(lambda x: (x,1))
print(wordPairs.collect())

# COMMAND ----------

# TEST Pair RDDs (1f)
Test.assertEquals(wordPairs.collect(),
                  [('cat', 1), ('elephant', 1), ('rat', 1), ('rat', 1), ('cat', 1)],
                  'incorrect value for wordPairs')

# COMMAND ----------

# MAGIC %md
# MAGIC #### ** Part 2: Counting with Pair RDDs **
# MAGIC 
# MAGIC Now, let's count the number of times a particular word appears in the RDD. There are multiple ways to perform the counting, but some are much less efficient than others.
# MAGIC 
# MAGIC A naive approach would be to `collect()` all of the elements and count them in the driver program. While this approach could work for small datasets, we want an approach that will work for any size dataset including terabyte- or petabyte-sized datasets. In addition, performing all of the work in the driver program is slower than performing it in parallel in the workers. For these reasons, we will use data parallel operations.
# MAGIC 
# MAGIC ** (2a) `groupByKey()` approach **
# MAGIC 
# MAGIC An approach you might first consider (we'll see shortly that there are better ways) is based on using the [groupByKey()](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.RDD.groupByKey.html) transformation. As the name implies, the `groupByKey()` transformation groups all the elements of the RDD with the same key into a single list in one of the partitions. There are two problems with using `groupByKey()`:
# MAGIC   + The operation requires a lot of data movement to move all the values into the appropriate partitions.
# MAGIC   + The lists can be very large. Consider a word count of English Wikipedia: the lists for common words (e.g., the, a, etc.) would be huge and could exhaust the available memory in a worker.
# MAGIC  
# MAGIC Use `groupByKey()` to generate a pair RDD of type `('word', iterator)`.

# COMMAND ----------

# TODO: Replace <FILL IN> with appropriate code
# Note that groupByKey requires no parameters
wordsGrouped = wordPairs.groupByKey()
for key, value in wordsGrouped.collect():
    print('{0}: {1}'.format(key, list(value)))

# COMMAND ----------

# TEST groupByKey() approach (2a)
Test.assertEquals(sorted(wordsGrouped.mapValues(lambda x: list(x)).collect()),
                  [('cat', [1, 1]), ('elephant', [1]), ('rat', [1, 1])],
                  'incorrect value for wordsGrouped')

# COMMAND ----------

# MAGIC %md
# MAGIC ** (2b) Use `groupByKey()` to obtain the counts **
# MAGIC 
# MAGIC Using the `groupByKey()` transformation creates an RDD containing 3 elements, each of which is a pair of a word and a Python iterator.
# MAGIC 
# MAGIC Now sum the iterator using a `map()` transformation.  The result should be a pair RDD consisting of (word, count) pairs.

# COMMAND ----------

# TODO: Replace <FILL IN> with appropriate code
wordCountsGrouped = wordsGrouped.map(lambda x: (x[0], sum(x[1])))
print(wordCountsGrouped.collect())

# COMMAND ----------

# TEST Use groupByKey() to obtain the counts (2b)
Test.assertEquals(sorted(wordCountsGrouped.collect()),
                  [('cat', 2), ('elephant', 1), ('rat', 2)],
                  'incorrect value for wordCountsGrouped')

# COMMAND ----------

# MAGIC %md
# MAGIC ** (2c) Count using `reduceByKey` **
# MAGIC 
# MAGIC A better approach is to start from the pair RDD and then use the [reduceByKey()](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.RDD.reduceByKey.html) transformation to create a new pair RDD. The `reduceByKey()` transformation gathers together pairs that have the same key and applies the function provided to two values at a time, iteratively reducing all of the values to a single value. `reduceByKey()` operates by applying the function first within each partition on a per-key basis and then across the partitions, allowing it to scale efficiently to large datasets.

# COMMAND ----------

# TODO: Replace <FILL IN> with appropriate code
# Note that reduceByKey takes in a function that accepts two values and returns a single value
wordCounts = wordPairs.reduceByKey(lambda x,y : x+y)
print(wordCounts.collect())

# COMMAND ----------

# TEST Counting using reduceByKey (2c)
Test.assertEquals(sorted(wordCounts.collect()), [('cat', 2), ('elephant', 1), ('rat', 2)],
                  'incorrect value for wordCounts')

# COMMAND ----------

# MAGIC %md
# MAGIC ** (2d) All together **
# MAGIC 
# MAGIC The expert version of the code performs the `map()` to pair RDD, `reduceByKey()` transformation, and `collect` in one statement.

# COMMAND ----------

# TODO: Replace <FILL IN> with appropriate code
wordCountsCollected = (wordsRDD
                       .map(lambda x: (x,1))\
                       .reduceByKey(lambda x,y : x+y)\
                       .collect())
print(wordCountsCollected)

# COMMAND ----------

# TEST All together (2d)
Test.assertEquals(sorted(wordCountsCollected), [('cat', 2), ('elephant', 1), ('rat', 2)],
                  'incorrect value for wordCountsCollected')

# COMMAND ----------

# MAGIC %md
# MAGIC #### ** Part 3: More Transformations **
# MAGIC 
# MAGIC ** (3a) Unique words **
# MAGIC 
# MAGIC Calculate the number of unique words in `wordsRDD`.  You can use other RDDs that you have already created to make this easier.

# COMMAND ----------

# TODO: Replace <FILL IN> with appropriate code
uniqueWords = wordCounts.map(lambda x: x[0]).count()
print(uniqueWords)

# COMMAND ----------

# TEST Unique words (3a)
Test.assertEquals(uniqueWords, 3, 'incorrect count of uniqueWords')

# COMMAND ----------

# MAGIC %md
# MAGIC ** (3b) Calculate mean using `reduce` **
# MAGIC 
# MAGIC Find the mean number of words per unique word in `wordCounts`.
# MAGIC 
# MAGIC Use a `reduce()` action to sum the counts in `wordCounts` and then divide by the number of unique words.  First `map()` the pair RDD `wordCounts`, which consists of (key, value) pairs, to an RDD of values.

# COMMAND ----------

wordCounts.collect()

# COMMAND ----------

# TODO: Replace <FILL IN> with appropriate code
from operator import add
totalCount = (wordCounts
              .map(lambda x:x[1])\
              .reduce(lambda x,y: x+y))
average = totalCount / float(wordCounts.count())
print(totalCount)
print(round(average, 2))

# COMMAND ----------

# TEST Mean using reduce (3b)
Test.assertEquals(round(average, 2), 1.67, 'incorrect value of average')

# COMMAND ----------

# MAGIC %md
# MAGIC #### ** Part 4: Applying to a File **
# MAGIC 
# MAGIC In this section we will finish developing our word count application.  We'll have to build the `wordCount` function, deal with real world problems like capitalization and punctuation, load in our data source, and compute the word count on the new data.
# MAGIC 
# MAGIC ** (4a) `wordCount` function **
# MAGIC 
# MAGIC First, define a function for word counting.  You should reuse the techniques that have been covered in earlier parts of this lab.  This function should take in an RDD that is a list of words like `wordsRDD` and return a pair RDD that has all of the words and their associated counts.

# COMMAND ----------

# TODO: Replace <FILL IN> with appropriate code
def wordCount(wordListRDD):
    """Creates a pair RDD with word counts from an RDD of words.

    Args:
        wordListRDD (RDD of str): An RDD consisting of words.

    Returns:
        RDD of (str, int): An RDD consisting of (word, count) tuples.
    """
    return wordListRDD.map(lambda x: (x,1))\
                    .reduceByKey(lambda x,y : x+y)

print(wordCount(wordsRDD).collect())

# COMMAND ----------

# TEST wordCount function (4a)
Test.assertEquals(sorted(wordCount(wordsRDD).collect()),
                  [('cat', 2), ('elephant', 1), ('rat', 2)],
                  'incorrect definition for wordCount function')

# COMMAND ----------

# MAGIC %md
# MAGIC ** (4b) Capitalization and punctuation **
# MAGIC 
# MAGIC Real world files are more complicated than the data we have been using in this lab. Some of the issues we have to address are:
# MAGIC   + Words should be counted independent of their capitialization (e.g., Spark and spark should be counted as the same word).
# MAGIC   + All punctuation should be removed.
# MAGIC   + Any leading or trailing spaces on a line should be removed.
# MAGIC  
# MAGIC Define the function `removePunctuation` that converts all text to lower case, removes any punctuation, and removes leading and trailing spaces.  Use the Python [re](https://docs.python.org/2/library/re.html) module to remove any text that is not a letter, number, or space. Reading `help(re.sub)` might be useful.

# COMMAND ----------

# TODO: Replace <FILL IN> with appropriate code
import re
def removePunctuation(text):
    """Removes punctuation, changes to lower case, and strips leading and trailing spaces.

    Note:
        Only spaces, letters, and numbers should be retained.  Other characters should should be
        eliminated (e.g. it's becomes its).  Leading and trailing spaces should be removed after
        punctuation is removed.

    Args:
        text (str): A string.

    Returns:
        str: The cleaned up string.
    """
    
    return re.sub(r'[^a-z0-9\s]','',string = text.lower().strip())
    
print(removePunctuation('Hi, you!'))
print(removePunctuation(' No under_score!'))

# COMMAND ----------

# TEST Capitalization and punctuation (4b)
Test.assertEquals(removePunctuation(" The Elephant's 4 cats. "),
                  'the elephants 4 cats',
                  'incorrect definition for removePunctuation function')

# COMMAND ----------

# MAGIC %md
# MAGIC ** (4c) Load a text file **
# MAGIC 
# MAGIC For the next part of this lab, we will use the [Complete Works of William Shakespeare](http://www.gutenberg.org/ebooks/100) from [Project Gutenberg](http://www.gutenberg.org). To convert a text file into an RDD, we use the `SparkContext.textFile()` method. We also apply the recently defined `removePunctuation()` function using a `map()` transformation to strip out the punctuation and change all text to lowercase.  Since the file is large we use `take(15)`, so that we only print 15 lines.
# MAGIC 
# MAGIC **WARNING**: If you haven't uploaded the text file as instructed in the warmup notebook, please upload it before running the cell below.

# COMMAND ----------

# Just run this code
import os.path
filePath = 'dbfs:/FileStore/tables/shakespere.txt'
# filePath = 'shakespere.txt'

shakespeareRDD = (sc
                  .textFile(filePath, 8)
                  .map(removePunctuation))
print('\n'.join(shakespeareRDD
                .zipWithIndex() # to (line, lineNum)
                .map(lambda s: '{0}: {1}'.format(s[1], s[0])) # to 'lineNum: line'
                .take(15)))

# COMMAND ----------

# MAGIC %md
# MAGIC ** (4d) Words from lines **
# MAGIC 
# MAGIC Before we can use the `wordcount()` function, we have to split each line by its spaces. Apply a transformation that will split each element of the RDD by its spaces. For each element of the RDD, you should apply Python's string [split()](https://docs.python.org/3/library/string.html#string.split) function. You might think that a `map()` transformation is the way to do this, but think about what the result of the `split()` function will be.

# COMMAND ----------

# TODO: Replace <FILL IN> with appropriate code
shakespeareWordsRDD = shakespeareRDD.flatMap(lambda x: [i for i in x.split()])
shakespeareWordCount = shakespeareWordsRDD.count()
print(shakespeareWordsRDD.top(5))
print(shakespeareWordCount)

# COMMAND ----------

# TEST Words from lines (4d)
Test.assertTrue(shakespeareWordCount == 959524,
                'incorrect value for shakespeareWordCount')
Test.assertEquals(shakespeareWordsRDD.top(5),
                  [u'zwounds', u'zwounds', u'zwounds', u'zwounds', u'zwounds'],
                  'incorrect value for shakespeareWordsRDD')


# COMMAND ----------

# MAGIC %md
# MAGIC ** (4e) Count the words **
# MAGIC 
# MAGIC We now have an RDD that is only words.  Next, let's apply the `wordCount()` function to produce a list of word counts. We can view the top 10 words by using the `takeOrdered()` action; however, since the elements of the RDD are pairs, we need a custom sort function that sorts using the value part of the pair.
# MAGIC 
# MAGIC You'll notice that many of the words are common English words. These are called stopwords. In a later lab, we will see how to eliminate them from the results.
# MAGIC 
# MAGIC Use the `wordCount()` function and `takeOrdered()` to obtain the fifteen most common words and their counts.

# COMMAND ----------

# TODO: Replace <FILL IN> with appropriate code
top10WordsAndCounts = wordCount(shakespeareWordsRDD).takeOrdered(10,key=lambda x: -x[1])
print('\n'.join(map(lambda s: '{0}: {1}'.format(s[0], s[1]), top10WordsAndCounts)))

# COMMAND ----------

# TEST Count the words (4f)
Test.assertEquals(top10WordsAndCounts,
                  [(u'the', 30018), (u'and', 28358), (u'i', 21868), (u'to', 20890), 
                   (u'of', 18815), (u'a', 16000), (u'you', 14438), (u'my', 13191), 
                   (u'in', 12034), (u'that', 11781)],
                  'incorrect value for top10WordsAndCounts')
