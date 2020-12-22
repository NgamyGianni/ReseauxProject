import java.io.*;
public class test {
    public static void main(String[] args) throws FileNotFoundException{
     
        BufferedReader in = new BufferedReader(new FileReader("a.txt"));
            
        String base = "";
            try {
                base+= ""+in.read();
                base+= ""+in.read();
                base+= ""+in.read();
                base+= ""+in.read();}
                catch(IOException ex) {
                    System.out.println("Erreur lors de la lecture");
                }
        String fin ="";
            try {
                fin += in.readLine();}
                catch(IOException ex) {
                    System.out.println("Erreur lors de la lecture");
                }
        System.out.println(base+fin);
        }
}
