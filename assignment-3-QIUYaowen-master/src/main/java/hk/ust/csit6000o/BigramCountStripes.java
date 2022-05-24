package hk.ust.csit6000o;

import java.io.IOException;
import java.util.Arrays;
import java.util.HashSet; //import
import java.util.Set; //import

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.GnuParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.OptionBuilder;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
import org.apache.log4j.Logger;

/**
 * Compute the bigram count using the "stripes" approach
 */
public class BigramCountStripes extends Configured implements Tool {
	private static final Logger LOG = Logger
			.getLogger(BigramCountStripes.class);

	/*
	 * Mapper: emits <word, stripe> where stripe is a hash map
	 */
	private static class MyMapper extends
			Mapper<LongWritable, Text, Text, HashMapStringIntWritable> {

		// Reuse objects to save overhead of object creation.
		private static final Text KEY = new Text();
		private static final HashMapStringIntWritable STRIPE = new HashMapStringIntWritable();
		private static final Set<String> set= new HashSet<String>();

		@Override
		public void map(LongWritable key, Text value, Context context)
				throws IOException, InterruptedException {
			String line = ((Text) value).toString();
			String[] words = line.trim().split("\\s+");

			/*
			 * TODO: Your implementation goes here
			 */

			set.clear(); //clear set, same as below

			for (int i = 0; i < words.length - 1; i++) {
				if (set.contains(words[i])){
					continue;
				}
				else{
					STRIPE.clear();

					set.add(words[i]);
					KEY.set(words[i]);

					for (int j = i + 1; j < words.length; j++)
						if (words[j - 1].equals(words[i])){
							STRIPE.increment(words[j]);
						}
							
					context.write(KEY, STRIPE);
				}


			}

			
		}
	}

	/*
	 * Reducer: aggregate all stripes associated with each key
	 */
	private static class MyReducer extends
			Reducer<Text, HashMapStringIntWritable, PairOfStrings, IntWritable> {

		// Reuse objects.
		private final static HashMapStringIntWritable SUM_STRIPES = new HashMapStringIntWritable();
		private final static PairOfStrings BIGRAM = new PairOfStrings();
		private final static IntWritable COUNT = new IntWritable();

		@Override
		public void reduce(Text key,
				Iterable<HashMapStringIntWritable> stripes, Context context)
				throws IOException, InterruptedException {
			/*
			 * TODO: Your implementation goes here. Hint: You can add up two
			 * stripes using the plus() method. Please refer to the
			 * implementation of HashMapStringIntWritable for details.
			 */

			/*
			 * The output must be a sequence of key-value pairs of <bigram,
			 * count>, the same as that of the "pairs" approach
			 */

			SUM_STRIPES.clear();

			for (HashMapStringIntWritable stripe : stripes){
				SUM_STRIPES.plus(stripe);
			}
				
			Set<String> keys = SUM_STRIPES.keySet();
			String key_string = key.toString();

			for (String value : keys) {
				BIGRAM.set(key_string, value);

				COUNT.set(SUM_STRIPES.get(value));

				context.write(BIGRAM, COUNT);
			}

		}
	}

	/*
	 * Combiner: aggregate all stripes
	 */
	private static class MyCombiner
			extends
			Reducer<Text, HashMapStringIntWritable, Text, HashMapStringIntWritable> {
		// Reuse objects.
		private final static HashMapStringIntWritable SUM_STRIPES = new HashMapStringIntWritable();

		@Override
		public void reduce(Text key,
				Iterable<HashMapStringIntWritable> stripes, Context context)
				throws IOException, InterruptedException {
			/*
			 * TODO: Your implementation goes here
			 */
			SUM_STRIPES.clear();
			for (HashMapStringIntWritable stripe : stripes){
				SUM_STRIPES.plus(stripe);
			}
				
			context.write(key, SUM_STRIPES);
			
		}
	}

	/**
	 * Creates an instance of this tool.
	 */
	public BigramCountStripes() {
	}

	private static final String INPUT = "input";
	private static final String OUTPUT = "output";
	private static final String NUM_REDUCERS = "numReducers";

	/**
	 * Runs this tool.
	 */
	@SuppressWarnings({ "static-access" })
	public int run(String[] args) throws Exception {
		Options options = new Options();

		options.addOption(OptionBuilder.withArgName("path").hasArg()
				.withDescription("input path").create(INPUT));
		options.addOption(OptionBuilder.withArgName("path").hasArg()
				.withDescription("output path").create(OUTPUT));
		options.addOption(OptionBuilder.withArgName("num").hasArg()
				.withDescription("number of reducers").create(NUM_REDUCERS));

		CommandLine cmdline;
		CommandLineParser parser = new GnuParser();

		try {
			cmdline = parser.parse(options, args);
		} catch (ParseException exp) {
			System.err.println("Error parsing command line: "
					+ exp.getMessage());
			return -1;
		}

		// Lack of arguments
		if (!cmdline.hasOption(INPUT) || !cmdline.hasOption(OUTPUT)) {
			System.out.println("args: " + Arrays.toString(args));
			HelpFormatter formatter = new HelpFormatter();
			formatter.setWidth(120);
			formatter.printHelp(this.getClass().getName(), options);
			ToolRunner.printGenericCommandUsage(System.out);
			return -1;
		}

		String inputPath = cmdline.getOptionValue(INPUT);
		String outputPath = cmdline.getOptionValue(OUTPUT);
		int reduceTasks = cmdline.hasOption(NUM_REDUCERS) ? Integer
				.parseInt(cmdline.getOptionValue(NUM_REDUCERS)) : 1;

		LOG.info("Tool: " + BigramCountStripes.class.getSimpleName());
		LOG.info(" - input path: " + inputPath);
		LOG.info(" - output path: " + outputPath);
		LOG.info(" - number of reducers: " + reduceTasks);

		// Create and configure a MapReduce job
		Configuration conf = getConf();
		Job job = Job.getInstance(conf);
		job.setJobName(BigramCountStripes.class.getSimpleName());
		job.setJarByClass(BigramCountStripes.class);

		job.setNumReduceTasks(reduceTasks);

		FileInputFormat.setInputPaths(job, new Path(inputPath));
		FileOutputFormat.setOutputPath(job, new Path(outputPath));

		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(HashMapStringIntWritable.class);
		job.setOutputKeyClass(PairOfStrings.class);
		job.setOutputValueClass(IntWritable.class);

		/*
		 * A MapReduce program consists of four components: a mapper, a reducer,
		 * an optional combiner, and an optional partitioner.
		 */
		job.setMapperClass(MyMapper.class);
		job.setCombinerClass(MyCombiner.class);
		job.setReducerClass(MyReducer.class);

		// Delete the output directory if it exists already.
		Path outputDir = new Path(outputPath);
		FileSystem.get(conf).delete(outputDir, true);

		// Time the program
		long startTime = System.currentTimeMillis();
		job.waitForCompletion(true);
		LOG.info("Job Finished in " + (System.currentTimeMillis() - startTime)
				/ 1000.0 + " seconds");

		return 0;
	}

	/**
	 * Dispatches command-line arguments to the tool via the {@code ToolRunner}.
	 */
	public static void main(String[] args) throws Exception {
		ToolRunner.run(new BigramCountStripes(), args);
	}
}
