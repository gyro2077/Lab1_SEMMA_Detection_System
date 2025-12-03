// Java deserialization
import java.io.*;

public class DataLoader {
    public Object loadObject(byte[] data) throws Exception {
        // VULNERABLE: Deserializing untrusted data
        ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(data));
        return ois.readObject();
    }
}
