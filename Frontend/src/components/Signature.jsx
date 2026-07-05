import { motion } from "framer-motion";

function Signature() {
  return (
    <motion.div
      animate={{
        x: [-300, 300, -300],
      }}
      transition={{
        repeat: Infinity,
        duration: 12,
        ease: "linear",
      }}
      style={styles.container}
    >
      ✍️ Made with ❤️ by
      <span style={styles.name}>
        {" "}
        Zeeya Sinha
      </span>
    </motion.div>
  );
}

const styles = {
  container: {
    marginTop: "35px",
    fontSize: "22px",
    fontWeight: "700",
    color: "gold",
    whiteSpace: "nowrap",
    overflow: "hidden",
  },

  name: {
    color: "#fff",
    fontSize: "28px",
    fontFamily: "cursive",
  },
};

export default Signature;