package shellcuts

import java.nio.charset.StandardCharsets
import shellcuts.core.{
  Configuration,
  CrumbOperation,
  DefaultFollowOperation,
  DeleteOperation,
  Encoding,
  GoOperation,
  HelpOperation,
  NewOperation,
  Parsing,
  Shellcut
}

object Main {
  val DefaultCharset = StandardCharsets.UTF_8
  val ConfigurationFile = "/tmp/junkjunkjunkjunk"
  val BigDelimiter = "\0\0\0"
  val SmallDelimiter = "\0"
  val GlobalsPattern = """^([^\0]*)\0([^\0]*)""".r
  val ShellcutPattern = """\0\0\0([^\0]+)\0([^\0]*)((?:\0[^\0]+)+)""".r
  val PathPattern = """\0([^\0]+)""".r
  val HomeProperty = "user.home"
  val CurrentDirProperty = "user.dir"
  val Operations = Map(
    "-n" -> NewOperation,
    "--new" -> NewOperation,
    "--default-follow" -> DefaultFollowOperation,
    "-d" -> DeleteOperation,
    "--delete" -> DeleteOperation
  )

  def main(arguments: Array[String]): Unit = {

    // Parse the input arguments. This will produce an operation and all
    // necessary parameters for that operation.
    def parse = Parsing.parse(
      CrumbOperation,
      GoOperation,
      HelpOperation,
      Operations
    ) _
    val (operation, parameters) = parse(arguments)

    // Retrieve relevant system properties that may be required by the
    // operation.
    val properties = Unsafe.fetchProperties(HomeProperty, CurrentDirProperty)

    // Load the program configuration from the configuration file.
    val decode = Encoding.decode(
      GlobalsPattern,
      ShellcutPattern,
      PathPattern
    ) _
    val load = Unsafe.load(DefaultCharset) _
    val originalConfig = load(ConfigurationFile).right map {
      (raw) => decode(raw)
    }

    // Modify the configuration via the given operation's modify() function.
    val modifiedConfig = (properties, originalConfig) match {
      case (Right(properties), Right(originalConfig)) => {
        operation.modify(originalConfig, properties, parameters)
      }
      case (Left(message), _) => Left(message)
      case (_, Left(message)) => Left(message)
    }

    print(modifiedConfig)

    // Retrieve the appropriate return command for the given operation.
    val command = (properties, modifiedConfig) match {
      case (Right(properties), Right(modifiedConfig)) => {
        Right(operation.command(modifiedConfig, properties, parameters))
      }
      case (Left(message), _) => Left(message)
      case (_, Left(message)) => Left(message)
    }

    // Write the modified configuration to the configuration file.
    val encode = Encoding.encode(
      BigDelimiter,
      SmallDelimiter,
      DefaultCharset
    ) _
    val dump = Unsafe.dump(DefaultCharset) _
    val result = modifiedConfig.right flatMap {
      (config) => dump(ConfigurationFile, encode(config))
    }

    // Error messages propagate through this function as Lefts. If any lefts
    // exist, print the error message. Otherwise, print the successfully
    // generated return command.
    (command, result) match {
      case (Left(message), _) => print(message)
      case (_, Left(message)) => print(message)
      case (Right(command), Right(result)) => print(command)
    }
  }
}
