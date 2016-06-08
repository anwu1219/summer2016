import java.util.*;
import java.io.*;

class findRank{
  public static void main(String[] args) throws IOException{
    Scanner sc = new Scanner(new File(args[0]));
    while (sc.hasNextLine()){
      sc.nextLine(); 
      double timeMini = sc.nextDouble();
      int pickedRidge = sc.nextInt(), pickedForest = sc.nextInt(), cntMini = 0, cntRidge = 0, cntForest = 0;
      sc.nextLine();
      double[] time = new double[300];
      for (int i = 0; i < 300; i++){
        String[] line = sc.nextLine().split(" ");
        double t1 = Double.parseDouble(line[1]), t2 = Double.parseDouble(line[3]), t;
        if (line[2].equals("True") && line[4].equals("True")){
          t = t1/2 + t2/2;
        } else if (line[2].equals("True") && line[4].equals("False")){
          t = t1 + t2/2;
        } else if (line[2].equals("False") && line[4].equals("True")){
          t = t1/2 + t2;
        } else {
          t = t1 + t2;
        }
        time[i] = t;
      }
      double timeRidge = time[pickedRidge-1], timeForest = time[pickedForest-1];
      
      for (double temp: time){
        if (temp < timeMini){
          cntMini++;
        }
        if (temp < timeRidge){
          cntRidge++;
        }
        if (temp < timeForest){
          cntForest++;
        }
      }
      System.out.format("%.2f, %d, %.2f, %d,%.2f, %d\n", timeMini, cntMini, timeRidge, cntRidge, timeForest,cntForest);
    }
  }
}
        
          