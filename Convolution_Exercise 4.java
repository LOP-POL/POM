import java.util.Arrays;

public class Convolution {
	public static void main(String[] args) {
		double[][] A = {
						   { 0, 60, 120, 180, 240, 300, 360 },
						   { 0, 0.2, 0.3, 0.1, 0.2, 0.1, 0.1 }
					   };

		double[][] B = {
						   { 0, 60, 120, 180, 240, 300, 360 },
						   { 0.1, 0.2, 0.4, 0.1, 0.2, 0, 0.0 }
					   };

		double[][] C = {
						   { 0, 60, 120, 180, 240, 300, 360 },
						   { 0.1, 0, 0.4, 0.4, 0, 0.1, 0 }
					   };

		double[][] D = {
						   { 0, 60, 120, 180, 240, 300, 360 },
						   { 0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1 }
					   };

		double[] Size = { 0.006, 0.010, 0.012, 0.015 };

		double[][] meanA = MeanSize(A, Size);
		double[][] meanB = MeanSize(B, Size);
		double[][] meanC = MeanSize(C, Size);
		double[][] meanD = MeanSize(D, Size);

		double[][] exerciseB = Convolution(Convolution(Convolution(meanA, meanB),
		meanC),
		meanD);

		System.out.println("B (mean)");

		System.out.println("Exercise B (mean)");
		System.out.println("Volume | Probability | Cumulative Probability");

		double cumulative = 0;

		for (int i = 0; i < exerciseB[0].length; i++) {
			cumulative += exerciseB[1][i];
			System.out.printf("%.4f | %.4f | %.4f%n", exerciseB[0][i],
							  exerciseB[1][i], cumulative);
		}

		System.out.println();
		System.out.println();

		double[][] specificA = SpecificSize(A, Size[0]);
		double[][] specificB = SpecificSize(B, Size[1]);
		double[][] specificC = SpecificSize(C, Size[2]);
		double[][] specificD = SpecificSize(D, Size[3]);

		double[][] specificExerciseB = Convolution(Convolution(Convolution(specificA,specificB),
		specificC),
		specificD);

		System.out.println("B' (specific)");
		System.out.println("Volume | Probability | Cumulative Probability");

		double cumulativeSpecific = 0;

		for (int i = 0; i < specificExerciseB[0].length; i++) {
			cumulativeSpecific += specificExerciseB[1][i];
			System.out.printf("%.4f | %.4f | %.4f%n", specificExerciseB[0][i],
							  specificExerciseB[1][i], cumulativeSpecific);
		}
	}

	public static double[][] Convolution(double[][] x, double[][] y) {
		double[] Volume = possibleAdditions(x, y);

		double[] resulting_p = new double[Volume.length];

		for (int i = 0; i < Volume.length; i++) {
			for (int j = 0; j < x[0].length; j++) {
				for (int k = y[0].length - 1; k >= 0; k--) {
					if ((x[0][j] + y[0][k]) == Volume[i]) {
						resulting_p[i] += (x[1][j] * y[1][k]);
					}
				}
			}
		}

		double[][] result = new double[2][Volume.length];

		for (int i = 0; i < Volume.length; i++) {
			result[0][i] = Volume[i];
			result[1][i] = resulting_p[i];
		}

		sortResult(result);

		return result;
	}

	public static double[] possibleAdditions(double[][] x, double[][] y) {
		double[] tempSums = new double[x[0].length * y[0].length];

		int index = 0;

		for (int i = 0; i < x[0].length; i++) {
			for (int j = 0; j < y[0].length; j++) {
				tempSums[index] = x[0][i] + y[0][j];
				index++;
			}
		}

		// Remove duplicates from tempSums (simple approach)
		// Count unique sums
		int uniqueCount = 0;

		for (int i = 0; i < tempSums.length; i++) {
			boolean isDuplicate = false;

			for (int j = 0; j < i; j++) {
				if (tempSums[i] == tempSums[j]) {
					isDuplicate = true;

					break;
				}
			}

			if (!isDuplicate) {
				uniqueCount++;
			}
		}

		// Create array for unique sums
		double[] uniqueSums = new double[uniqueCount];
		int uniqueIndex = 0;

		for (int i = 0; i < tempSums.length; i++) {
			boolean isDuplicate = false;

			for (int j = 0; j < i; j++) {
				if (tempSums[i] == tempSums[j]) {
					isDuplicate = true;

					break;
				}
			}

			if (!isDuplicate) {
				uniqueSums[uniqueIndex] = tempSums[i];
				uniqueIndex++;
			}
		}

		return uniqueSums;
	}

	public static double[][] SpecificSize(double[][] x, double size) {
		double[][] specificX = new double[x.length][x[0].length];

		for (int i = 0; i < x[0].length; i++) {
			specificX[0][i] = x[0][i] * size;
			specificX[1][i] = x[1][i];
		}

		return specificX;
	}

	public static double[][] MeanSize(double[][] x, double[] size) {
		double[][] meanX = new double[x.length][x[0].length];

		double meanSize = (size[0] + size[1] + size[2] + size[3]) / 4;

		for (int i = 0; i < x[0].length; i++) {
			meanX[0][i] = x[0][i] * meanSize;
			meanX[1][i] = x[1][i];
		}

		return meanX;
	}

	public static void sortResult(double[][] result) {
	    // Create an array of indices [0, 1, 2, ...]
	    Integer[] indices = new Integer[result[0].length];
	    for (int i = 0; i < indices.length; i++) {
	        indices[i] = i;
	    }
	
	    // Sort indices based on the values in result[0] (volumes)
	    Arrays.sort(indices, (i, j) -> Double.compare(result[0][i], result[0][j]));
	
	    // Create sorted copies of volumes and probabilities
	    double[] sortedVolumes = new double[result[0].length];
	    double[] sortedProbabilities = new double[result[1].length];
	
	    for (int i = 0; i < indices.length; i++) {
	        sortedVolumes[i] = result[0][indices[i]];
	        sortedProbabilities[i] = result[1][indices[i]];
	    }
	
	    // Copy sorted results back into the original array
	    System.arraycopy(sortedVolumes, 0, result[0], 0, sortedVolumes.length);
	    System.arraycopy(sortedProbabilities, 0, result[1], 0, sortedProbabilities.length);
	}
}