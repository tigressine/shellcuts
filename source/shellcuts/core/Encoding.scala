package shellcuts.core

import java.nio.charset.Charset
import shellcuts.core.structures.{
  Configuration,
  Shellcut
}

object Encoding {
  val SmallDelimiter = "\0"
  val BigDelimiter = "\0\0\0"
  val GlobalsPattern = """^([^\u0000]*)\0([^\u0000]*)""".r
  val ShellcutPattern = """\0\0\0([^\u0000]+)\0([^\u0000]*)\0([^\u0000]+)""".r

  // Decode a configuration string into a Configuration object.
  def decode(encoded: String): Configuration = {
    val (crumb, defaultFollow) = GlobalsPattern.findFirstIn(encoded) map {
      case GlobalsPattern(crumb, defaultFollow) => (
        if (crumb.isEmpty) None else Some(crumb),
        if (defaultFollow.isEmpty) None else Some(defaultFollow)
      )
    } getOrElse((None, None))

    val shellcuts = ShellcutPattern.findAllIn(encoded).toList map {
      case ShellcutPattern(name, follow, path) => {
        Shellcut(name, if (follow.isEmpty) None else Some(follow), path)
      }
    }

    Configuration(crumb, defaultFollow, shellcuts)
  }

  // Encode a Configuration object into a configuration string.
  def encode(charset: Charset)(configuration: Configuration): String = {
    val head = configuration.crumb.getOrElse("") +
      SmallDelimiter +
      configuration.defaultFollow.getOrElse("")

    val body = configuration.shellcuts map {
      (shellcut) => {
        shellcut.name +
        SmallDelimiter +
        shellcut.follow.getOrElse("") +
        SmallDelimiter +
        shellcut.path
      }
    } mkString(BigDelimiter)

    if (body.isEmpty) {
      head
    } else {
      head + BigDelimiter + body
    }
  }
}
