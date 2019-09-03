package shellcuts.core

trait Operation {
  def modify(
    configuration: Configuration,
    properties: List[String],
    parameters: List[String]):
    Either[String, Configuration]

  def command(
    configuration: Configuration,
    properties: List[String],
    parameters: List[String]):
    String
}

object NewOperation extends Operation {
  override def modify(
    configuration: Configuration,
    properties: List[String],
    parameters: List[String]):
    Either[String, Configuration] = {

    if (parameters.length < 3) {
      return Left("No params")
    }

    val shellcut = Shellcut(
      parameters(0),
      Option(parameters(1)),
      List(parameters(2))
    )
    val shellcuts = configuration.shellcuts filter {
      (shellcut) => shellcut.name != parameters(0)
    } toList

    Right(
      Configuration(
        configuration.crumb,
        configuration.defaultFollow,
        shellcut :: shellcuts
      )
    )
  }

  override def command(
    configuration: Configuration,
    properties: List[String],
    parameters: List[String]):
    String = {

    "gooble"
  }
}

object DefaultFollowOperation extends Operation {
  override def modify(
    configuration: Configuration,
    properties: List[String],
    parameters: List[String]):
    Either[String, Configuration] = {

    if (parameters.length < 1) {
      Left("Missing follow command.")
    } else {
      Right(
        Configuration(
          configuration.crumb,
          Some(parameters(0)),
          configuration.shellcuts
        )
      )
    }
  }

  override def command(
    configuration: Configuration,
    properties: List[String],
    parameters: List[String]):
    String = {

    "defaultfollow"
  }
}

object CrumbOperation extends Operation {
  override def modify(
    configuration: Configuration,
    properties: List[String],
    parameters: List[String]):
    Either[String, Configuration] = {

    Right(configuration)
  }

  override def command(
    configuration: Configuration,
    properties: List[String],
    parameters: List[String]):
    String = {

    "crumb"
  }
}

object GoOperation extends Operation {
  override def modify(
    configuration: Configuration,
    properties: List[String],
    parameters: List[String]):
    Either[String, Configuration] = {

    Right(configuration)
  }

  override def command(
    configuration: Configuration,
    properties: List[String],
    parameters: List[String]):
    String = {

    "go"
  }
}

object DeleteOperation extends Operation {
  override def modify(
    configuration: Configuration,
    properties: List[String],
    parameters: List[String]):
    Either[String, Configuration] = {

    if (parameters.length < 1) {
      Left("Missing shellcut name.")
    } else {
      Right(
        Configuration(
          configuration.crumb,
          configuration.defaultFollow,
          configuration.shellcuts filter {
            (shellcut) => shellcut.name != parameters(0)
          } toList
        )
      )
    }
  }

  override def command(
    configuration: Configuration,
    properties: List[String],
    parameters: List[String]):
    String = {

    "delete"
  }
}

object HelpOperation extends Operation {
  override def modify(
    configuration: Configuration,
    properties: List[String],
    parameters: List[String]):
    Either[String, Configuration] = {

    Right(configuration)
  }

  override def command(
    configuration: Configuration,
    properties: List[String],
    parameters: List[String]):
    String = {

    "help"
  }
}
