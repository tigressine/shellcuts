package shellcuts

import java.nio.charset.StandardCharsets
import shellcuts.core.{
  Encoding,
  Parsing
}
import shellcuts.core.operations.{
  CrumbOperation,
  DeleteOperation,
  FollowOperation,
  GoOperation,
  HelpOperation,
  ListOperation,
  MoveOperation,
  NewOperation,
  RetraceOperation,
  UnfollowOperation,
  VersionOperation
}
import shellcuts.core.structures.{
  Configuration,
  Shellcut
}

object Main {
  val DefaultCharset = StandardCharsets.UTF_8
  val UnexpandedHomePattern = "^(~/.*|~)".r
  val DefaultConfigFile = "~/.shellcuts"
  val ConfigFileVariable = "SHELLCUTS_CONF"
  val HomeProperty = "user.home"
  val CurrentDirProperty = "user.dir"
  val Operations = Map(
    "-n" -> NewOperation,
    "--new" -> NewOperation,
    "-m" -> MoveOperation,
    "--move" -> MoveOperation,
    "-d" -> DeleteOperation,
    "--delete" -> DeleteOperation,
    "-c" -> CrumbOperation,
    "--crumb" -> CrumbOperation,
    "-f" -> FollowOperation,
    "--follow" -> FollowOperation,
    "-l" -> ListOperation,
    "--list" -> ListOperation,
    "-u" -> UnfollowOperation,
    "--unfollow" -> UnfollowOperation,
    "--version" -> VersionOperation
  )

  def main(arguments: Array[String]): Unit = {

    // Parse the input arguments. This will produce an operation and all
    // necessary parameters for that operation.
    def parse = Parsing.parse(
      RetraceOperation,
      GoOperation,
      HelpOperation,
      Operations
    ) _
    val (operation, parameters) = parse(arguments)

    // Retrieve relevant system properties that may be required by the
    // operation.
    val properties = IO.fetchProperties(HomeProperty, CurrentDirProperty)

    // Safely extract the home directory from the properties list.
    val homeDirectory = properties.right flatMap {
      (properties) => {
        properties.lift(0) match {
          case Some(property) => Right(property)
          case None => Left("home directory could not be determined")
        }
      }
    }

    // Use the configuration file path set by the user if available, else use
    // the default path. Expand the user's home directory as necessary.
    val configFile = (
      IO.fetchEnvironmentVariable(ConfigFileVariable) match {
        case Some(configFile) => configFile
        case None => DefaultConfigFile
      }
    ) match {
      case UnexpandedHomePattern(configFile) => homeDirectory.right map {
        (homeDirectory) => configFile.replaceFirst("~", homeDirectory)
      }
      case configFile => Right(configFile)
    }

    // Load the program configuration from the configuration file.
    val originalConfig = configFile.right flatMap {
      (configFile) => {
        val load = IO.load(DefaultCharset) _
        load(configFile).right map {
          (raw) => Encoding.decode(raw)
        }
      }
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
        operation.command(modifiedConfig, properties, parameters)
      }
      case (Left(message), _) => Left(message)
      case (_, Left(message)) => Left(message)
    }

    // Write the modified configuration to the configuration file.
    val result = modifiedConfig.right flatMap {
      (config) => {
        configFile.right flatMap {
          (configFile) => {
            val encode = Encoding.encode(DefaultCharset) _
            val dump = IO.dump(DefaultCharset) _
            dump(configFile, encode(config))
          }
        }
      }
    }

    // Error messages propagate through this function as Lefts. If any Lefts
    // exist, print the error message. Otherwise, offer the successfully
    // generated return command.
    (command, result) match {
      case (Left(message), _) => IO.error(message)
      case (_, Left(message)) => IO.error(message)
      case (Right(command), Right(result)) => IO.offer(command)
    }
  }
}
