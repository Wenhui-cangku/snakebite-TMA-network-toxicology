# Trend-plus-robust limma analysis and quantile-normalization sensitivity.
# Run from the archive 06_geo directory. Set LIMMA_OUT to avoid overwriting archived outputs.
library(limma)
INPUT <- 'limma_v2'
OUT <- Sys.getenv('LIMMA_OUT', 'limma_v2')
dir.create(OUT, recursive = TRUE, showWarnings = FALSE)

run_limma <- function(mat, group, treat_level, ctrl_level, tag) {
  group <- factor(group, levels = c(ctrl_level, treat_level))
  design <- model.matrix(~group)
  fit <- lmFit(mat, design)
  fit <- eBayes(fit, trend = TRUE, robust = TRUE)
  tt <- topTable(fit, coef = 2, number = Inf, adjust.method = 'BH', sort.by = 'P')
  tt$gene <- rownames(tt)
  write.csv(tt, file.path(OUT, paste0(tag, '_limma.csv')), row.names = FALSE)
  cat(tag, ': genes=', nrow(tt), ' BH<0.05=', sum(tt$adj.P.Val < 0.05),
      ' top=', tt$gene[1], '\n', sep = '')
  invisible(list(fit = fit, tt = tt))
}

g1 <- as.matrix(read.csv(file.path(INPUT, 'GSE121297_genelog2_matrix.csv'), row.names = 1))
grp1 <- c(rep('Ctrl', 3), rep('RCaB', 3))
r1 <- run_limma(g1, grp1, 'RCaB', 'Ctrl', 'GSE121297_RCaB_vs_Ctrl')
g1q <- normalizeBetweenArrays(g1, method = 'quantile')
r1q <- run_limma(g1q, grp1, 'RCaB', 'Ctrl', 'GSE121297_RCaB_vs_Ctrl_quantile_sens')

png(file.path(OUT, 'QC_GSE121297_boxplot_probelevel.png'), width = 1000, height = 700, res = 130)
pr <- as.matrix(read.csv(file.path(INPUT, 'GSE121297_probelevel_qc.csv'), row.names = 1))
boxplot(pr, las = 2, outline = FALSE, main = 'GSE121297 probe-level log2 intensity (GPL570)',
        ylab = 'log2 intensity', col = c(rep('grey70', 3), rep('lightblue', 3)))
dev.off()
png(file.path(OUT, 'QC_GSE121297_MDS.png'), width = 900, height = 700, res = 130)
plotMDS(g1, labels = colnames(g1), col = c(rep('black', 3), rep('red', 3)),
        main = 'GSE121297 MDS (gene-level log2)')
dev.off()
png(file.path(OUT, 'QC_GSE121297_phist.png'), width = 900, height = 700, res = 130)
hist(r1$tt$P.Value, breaks = 40, main = 'GSE121297 limma raw P distribution', xlab = 'raw P')
dev.off()
png(file.path(OUT, 'GSE121297_volcano_limma.png'), width = 950, height = 750, res = 130)
with(r1$tt, plot(logFC, -log10(P.Value), pch = 16, cex = 0.45,
                 main = 'GSE121297 RCaB vs Ctrl (limma)', xlab = 'log2FC', ylab = '-log10 raw P'))
with(subset(r1$tt, adj.P.Val < 0.05), points(logFC, -log10(P.Value), pch = 16, cex = 0.6, col = 'red'))
dev.off()

g2 <- as.matrix(read.csv(file.path(INPUT, 'GSE248215_normalized_log2.csv'), row.names = 1))
grp2 <- c(rep('DR24h', 3), rep('Ctrl', 2))
r2 <- run_limma(g2, grp2, 'DR24h', 'Ctrl', 'GSE248215_DR24h_vs_Ctrl')
png(file.path(OUT, 'QC_GSE248215_MDS.png'), width = 900, height = 700, res = 130)
plotMDS(g2, labels = colnames(g2), col = c(rep('red', 3), rep('black', 2)),
        main = 'GSE248215 MDS (log2 NanoString)')
dev.off()
png(file.path(OUT, 'GSE248215_volcano_limma.png'), width = 950, height = 750, res = 130)
with(r2$tt, plot(logFC, -log10(P.Value), pch = 16, cex = 0.8,
                 main = 'GSE248215 DR24h vs Ctrl (limma)', xlab = 'log2FC', ylab = '-log10 raw P'))
with(subset(r2$tt, adj.P.Val < 0.05), points(logFC, -log10(P.Value), pch = 16, cex = 0.9, col = 'red'))
dev.off()

writeLines(capture.output(sessionInfo()), file.path(OUT, 'R_session_info.txt'))
cat('DONE\n')
