package comp173.lab5;

/**
 *
 * @author julkata
 */

import java.net.*;
import java.io.*;
import java.nio.charset.Charset;

public class ServerB {
    
    public static void main(String[] args) throws IOException {
        ServerSocket s = new ServerSocket(Integer.parseInt(args[0]));
        
        while(true) {
            byte [] data = new byte[7];
            byte [] ready = "READY".getBytes(Charset.forName("ASCII"));
            
            Socket accept = s.accept();
            BufferedInputStream bin = new BufferedInputStream(accept.getInputStream());
            PrintWriter printerW = new PrintWriter(new PrintWriter(accept.getOutputStream(), true));
            
            DataOutputStream dos = new DataOutputStream(accept.getOutputStream());
            printerW.write("ready");
            printerW.flush();
            bin.read(data);
            
            int argLen = (data[1]) - 1;
            int leftMask = (int)Math.pow(2,4) -1;
            int result = (data[2] >> 4) & leftMask;

            int j = 2;
            
            for(int i = 0; i < argLen; i++){
                if(i%2 == 0){
                    if(data[0] == Math.pow(2,0)){
                        result += (data[j]) & leftMask;
                    }
                    else if(data[0] == Math.pow(2,1)){
                        result -= (data[j]) & leftMask;
                    }
                    else if(data[0] == Math.pow(2,2)){
                        result *= (data[j]) & leftMask;
                    }
                    j++;
                }
                else {
                    if(data[0] == Math.pow(2,0)){
                        result += (data[j] >> 4) & leftMask;
                    }
                    else if(data[0] == Math.pow(2, 1)){
                        result -= (data[j] >> 4) & leftMask;
                    }
                    else if(data[0] == Math.pow(2, 2)) {
                        result *= (data[j] >> 4) & leftMask;
                    }
                }
            }
            
            dos.writeInt(result);
            dos.flush();
        }
    }
}