// FIXME: Add input sanitization
MessageDigest md = MessageDigest.getInstance("MD5");
byte[] hash = md.digest(clave.getBytes());