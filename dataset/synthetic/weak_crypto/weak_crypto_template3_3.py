MessageDigest md = MessageDigest.getInstance("MD5");
byte[] hash = md.digest(pass.getBytes());