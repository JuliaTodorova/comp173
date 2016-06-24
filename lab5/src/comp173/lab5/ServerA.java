package comp173.lab5;

/**
 *
 * @author julkata
 */

import java.net.*;
import java.io.*;
import java.nio.charset.Charset;

public class ServerA {
    
    public static void main(String[] args) throws IOException {
        ServerSocket s = new ServerSocket(Integer.parseInt(args[0]));
        
        while(true) {
            byte [] data = new byte[7];
            byte [] ready = "READY".getBytes(Charset.forName("ASCII"));
            Socket accept = s.accept();
            
            BufferedInputStream bin = new BufferedInputStream(accept.getInputStream());
            BufferedOutputStream bos = new BufferedOutputStream(accept.getOutputStream());
            bos.write(ready);
            bos.flush();
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
            
            byte [] byteArray = new byte[4];

            int rightMask = (int) Math.pow(2, 8) -1;
            byteArray[0] = (byte) (rightMask & (result >> 24));
            byteArray[1] = (byte) (rightMask & (result >> 16));
            byteArray[2] = (byte) (rightMask & (result >> 8));
            byteArray[3] = (byte) (rightMask & result);

            bos.write(byteArray);
            bos.flush();
        }
    }
}