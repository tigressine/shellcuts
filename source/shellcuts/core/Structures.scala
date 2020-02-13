package shellcuts.core

case class Shellcut(name: String, follow: Option[String], paths: List[String])
case class Configuration(
  crumb: Option[String],
  defaultFollow: Option[String],
  shellcuts: List[Shellcut]
)
