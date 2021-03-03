import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.Arrays;

public class JavaUdpServer {

    public static void main(String args[])
    {
        System.out.println("JAVA UDP SERVER");
        DatagramSocket socket = null;
        int portNumber = 9008;

        try{
            socket = new DatagramSocket(portNumber);
            byte[] receiveBuffer = new byte[1024];

            while(true) {
                Arrays.fill(receiveBuffer, (byte)0);
                DatagramPacket receivePacket = new DatagramPacket(receiveBuffer, receiveBuffer.length);
                socket.receive(receivePacket);

                // decode msg as little edian
                int nb = ByteBuffer.wrap(receivePacket.getData()).order(ByteOrder.LITTLE_ENDIAN).getInt();
                System.out.println("received msg: " + nb);
                
                // add one and encode as little edian
                byte[] plusOne = ByteBuffer.allocate(4).order(ByteOrder.LITTLE_ENDIAN).putInt(nb + 1).array();

                // send encoded
                DatagramPacket plusOnePacket = new DatagramPacket(plusOne, plusOne.length,
                receivePacket.getAddress(), receivePacket.getPort());
                socket.send(plusOnePacket);
            }
        }
        catch(Exception e){
            e.printStackTrace();
        }
        finally {
            if (socket != null) {
                socket.close();
            }
        }
    }
}
