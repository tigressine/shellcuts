package shellcuts

import java.nio.charset.Charset
import java.nio.file.{
  Files,
  Paths,
  NoSuchFileException
}

object Unsafe {
  def load(charset: Charset)(path: String): Either[String, String] = {
    try {
      Right(new String(Files.readAllBytes(Paths.get(path)), charset))
    } catch {
      case exception: NoSuchFileException => Right("")
      case exception: IndexOutOfBoundsException => Right("")
      case exception: Exception => Left(exception.getMessage())
    }
  }

  def dump(charset: Charset)
          (path: String, content: String):
          Either[String, Unit] = {
    try {
      Right(Files.write(Paths.get(path), content.getBytes(charset)))
    } catch {
      case exception: Exception => Left(exception.getMessage())
    }
  }

  def fetchProperties(properties: String*): Either[String, List[String]] = {
    try {
      Right(
        properties map {
          (property) => System.getProperty(property)
        } toList
      )
    } catch {
      case exception: Exception => Left(exception.getMessage())
    }
  }
}
