package shellcuts

import java.nio.charset.StandardCharsets
import shellcuts.core.{
  Configuration,
  Encoding,
  Parsing,
  Shellcut
}
import shellcuts.core.operations.{
  DeleteOperation,
  GoOperation,
  HelpOperation,
  NewOperation
}

object Main {
  val DefaultCharset = StandardCharsets.UTF_8
  val ConfigurationFile = "/tmp/junkjunkjunkjunk"
  val HomeProperty = "user.home"
  val CurrentDirProperty = "user.dir"
  val Operations = Map(
    "-n" -> NewOperation,
    "--new" -> NewOperation,
    "-d" -> DeleteOperation,
    "--delete" -> DeleteOperation,
    "-h" -> HelpOperation,
    "--help" -> HelpOperation
  )

  def main(arguments: Array[String]): Unit = {

    // Parse the input arguments. This will produce an operation and all
    // necessary parameters for that operation.
    def parse = Parsing.parse(
      HelpOperation,
      GoOperation,
      HelpOperation,
      Operations
    ) _
    val (operation, parameters) = parse(arguments)

    // Retrieve relevant system properties that may be required by the
    // operation.
    val properties = IO.fetchProperties(HomeProperty, CurrentDirProperty)

    // Load the program configuration from the configuration file.
    val load = IO.load(DefaultCharset) _
    val originalConfig = load(ConfigurationFile).right map {
      (raw) => Encoding.decode(raw)
    }

    // Modify the configuration via the given operation's modify() function.
    val modifiedConfig = (properties, originalConfig) match {
      case (Right(properties), Right(originalConfig)) => {
        operation.modify(originalConfig, properties, parameters)
      }
      case (Left(message), _) => Left(message)
      case (_, Left(message)) => Left(message)
    }

    // Retrieve the appropriate return command for the given operation.
    val command = (properties, modifiedConfig) match {
      case (Right(properties), Right(modifiedConfig)) => {
        Right(operation.command(modifiedConfig, properties, parameters))
      }
      case (Left(message), _) => Left(message)
      case (_, Left(message)) => Left(message)
    }

    // Write the modified configuration to the configuration file.
    val encode = Encoding.encode(DefaultCharset) _
    val dump = IO.dump(DefaultCharset) _
    val result = modifiedConfig.right flatMap {
      (config) => dump(ConfigurationFile, encode(config))
    }

    // Error messages propagate through this function as Lefts. If any Lefts
    // exist, print the error message. Otherwise, print the successfully
    // generated return command.
    (command, result) match {
      case (Left(message), _) => print(message)
      case (_, Left(message)) => print(message)
      case (Right(command), Right(result)) => print(command)
    }
  }
}
