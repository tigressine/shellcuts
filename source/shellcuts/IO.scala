package shellcuts

import java.nio.charset.Charset
import java.nio.file.{
  Files,
  NoSuchFileException,
  Paths
}
import io.AnsiColor.{
  RED,
  RESET
}
import shellcuts.core.actions.PrintLineAction
import shellcuts.core.structures.Command

object IO {

  // Load the contents of a file as a string.
  def load(charset: Charset)(path: String): Either[String, String] = {
    try {
      Right(new String(Files.readAllBytes(Paths.get(path)), charset))
    } catch {
      case exception: NoSuchFileException => Right("")
      case exception: IndexOutOfBoundsException => Right("")
      case exception: Exception => Left(exception.getMessage())
    }
  }

  // Dump the contents of a string to a file.
  def dump(
    charset: Charset
  )(
    path: String,
    content: String
  ): Either[String, Unit] = {

    try {
      Right(Files.write(Paths.get(path), content.getBytes(charset)))
    } catch {
      case exception: Exception => Left(exception.getMessage())
    }
  }

  // Fetch system properties as a list.
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

  // Send an error to stdout.
  def error(message: String): Unit = {
    offer(Command(PrintLineAction, List(s"${RED}${message}${RESET}")))
  }

  // Offer a command to stdout.
  def offer(command: Command): Unit = {
    command.action.posixFormat(command.arguments) match {
      case Right(command) => print(command)
      case Left(message) => {
        print(PrintLineAction.posixFormat(List(message)).right)
      }
    }
  }
}
