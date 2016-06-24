package comp173.lab5;

/**
 *
 * @author julkata
 */

import java.net.*;
import java.io.*;

public class ClientB {
    public static final int MAXLEN = 14;

    public static void main(String[] args) throws IOException{
        String localHost = args[0];
        Integer port = Integer.parseInt(args[1]);
        String operation = args[2];
        
        byte [] data = new byte[7]; 
       
        if(operation.equals("+")) {
            data[0] = (byte) Math.pow(2,0);
        }
        else if(operation.equals("-")){
            data[0] = (byte) Math.pow(2,1);
        }
        else if(operation.equals("*")) {
            data[0] = (byte) Math.pow(2,2);
        }
        
        int count;

        if (args.length <= MAXLEN) {
            count = args.length - 3;
        }
        else {
            count = MAXLEN - 3;
        }

        data[1] = (byte) count;
        int j = 2;
        int argInt;
        for(int i = 0; i < count; i++) {
            if(i%2 == 0){
                argInt = Integer.parseInt(args[i + 3]);
                data[j] = (byte)(argInt << 4);
            }
            else {
                argInt = Integer.parseInt(args[i + 3]);
                data[j] |= argInt; 
                j++;
            }
        }

        Socket s = new Socket(localHost, port);
        BufferedReader buffer = new BufferedReader(new InputStreamReader(s.getInputStream()));
        BufferedOutputStream bos = new BufferedOutputStream(s.getOutputStream());
        DataInputStream dis = new DataInputStream(s.getInputStream());
        
        char [] ready = new char [5];
        buffer.read(ready);
        
        bos.write(data);
        bos.flush();    
        
        System.out.println(dis.readInt());
    }
}