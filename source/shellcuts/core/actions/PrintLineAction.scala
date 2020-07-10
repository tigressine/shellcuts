package shellcuts.core.actions

object PrintLineAction extends Action {
  override def posixFormat(arguments: List[String]): Either[String, String] = {
    if (arguments.length < 1) {
      Left("could not format command, no argument provided")
    } else {
      val cleanedArguments = arguments map {
        (argument) => argument.replace("'", "'\\''")
      }

      Right(s"printf '%s\\n' '${cleanedArguments.mkString("' '")}'")
    }
  }
}
